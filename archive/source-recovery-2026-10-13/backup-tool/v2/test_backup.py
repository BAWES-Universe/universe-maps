import copy
import json
import os
from pathlib import Path
import tempfile
import types
import io
import gzip
import unittest
from unittest.mock import patch
import universe_backup as u

class MemoryStore:
    def __init__(self):
        self.objects = {}
        self.events = []
        self.corrupt = None
        self.interrupt_at = None
        self.after_put = None
    def exists(self, key):
        self.events.append(('head', key))
        return key in self.objects
    def put_if_absent(self, key, data):
        self.events.append(('put', key))
        self.objects.setdefault(key, data)
        if self.after_put:
            self.after_put(key)
        if self.interrupt_at and key.startswith(self.interrupt_at):
            raise InterruptedError('simulated response loss after accepted PUT')
    def get(self, key, limit):
        self.events.append(('get', key))
        data = self.objects[key]
        if self.corrupt and key.startswith(self.corrupt):
            data = b'X' + data[1:]
        if len(data) > limit:
            raise u.Unsafe('oversize')
        return data

class BackupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.src = self.base / 'src'
        self.src.mkdir()
        (self.src / 'index.html').write_bytes(b'<html>Universe</html>')
        (self.src / 'art.svg').write_bytes(b'<svg/>')
        self.c = {'roots': {'map': str(self.src)}, 'max_total_bytes': 100000, 'max_file_bytes': 10000, 'max_files': 100, 'max_new_bytes': 100000, 'max_upload_operations': 300, 'extra_exclude': []}
        self.store = MemoryStore()
    def no_checkpoint(self):
        self.assertFalse(any(k.startswith('checkpoints/') for k in self.store.objects))
    def test_roundtrip_and_checkpoint_order(self):
        result = u.backup(self.c, self.store)
        events = self.store.events
        cpindex = next(i for i, e in enumerate(events) if e[0] == 'put' and e[1].startswith('checkpoints/'))
        for k in self.store.objects:
            if not k.startswith('checkpoints/'):
                self.assertIn(('get', k), events[:cpindex])
        dest = self.base / 'restore'
        r = u.restore(self.c, self.store, result['checkpoint'], dest)
        self.assertTrue(r['verified'])
        self.assertEqual((dest / 'map/index.html').read_bytes(), (self.src / 'index.html').read_bytes())
        self.assertEqual((dest / 'map/art.svg').stat().st_mode & 0o777, 0o600)
    def test_duplicate_content_uploaded_once(self):
        (self.src / 'duplicate.svg').write_bytes(b'<svg/>')
        r = u.backup(self.c, self.store)
        self.assertEqual(r['files'], 3)
        self.assertEqual(r['unique_objects'], 2)
        self.assertEqual(sum(e[0] == 'put' and e[1].startswith('objects/') for e in self.store.events), 2)
    def test_retry_idempotent_and_reverifies(self):
        r = u.backup(self.c, self.store)
        self.store.events = []
        again = u.backup(self.c, self.store)
        self.assertEqual(r['checkpoint'], again['checkpoint'])
        self.assertEqual(again['new_bytes'], 0)
        self.assertEqual(again['maximum_put_attempts'], 0)
        self.assertFalse(any(e[0] == 'put' for e in self.store.events))
        self.assertEqual(sum(e[0] == 'get' for e in self.store.events), 4)
    def test_interrupted_object_upload_retry(self):
        self.store.interrupt_at = 'objects/'
        with self.assertRaises(InterruptedError):
            u.backup(self.c, self.store)
        self.no_checkpoint()
        old = dict(self.store.objects)
        self.store.interrupt_at = None
        u.backup(self.c, self.store)
        for k, v in old.items():
            self.assertEqual(self.store.objects[k], v)
    def test_interrupted_checkpoint_readback_retry(self):
        self.store.interrupt_at = 'checkpoints/'
        with self.assertRaises(InterruptedError):
            u.backup(self.c, self.store)
        self.store.interrupt_at = None
        result = u.backup(self.c, self.store)
        u.restore(self.c, self.store, result['checkpoint'], self.base / 'restore')
    def test_corrupt_new_object_blocks_checkpoint(self):
        self.store.corrupt = 'objects/'
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.no_checkpoint()
    def test_corrupt_existing_object_never_overwritten(self):
        h = u.digest(b'<svg/>')
        key = 'objects/sha256/' + h
        self.store.objects[key] = b'WRONG!'
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.assertEqual(self.store.objects[key], b'WRONG!')
        self.no_checkpoint()
    def test_corrupt_manifest_blocks_checkpoint(self):
        self.store.corrupt = 'manifests/'
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.no_checkpoint()
    def test_changed_file_blocks_checkpoint(self):
        self.store.after_put = lambda _: (self.src / 'index.html').write_bytes(b'changed')
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.no_checkpoint()
    def test_deleted_file_blocks_checkpoint(self):
        def delete(_):
            f = self.src / 'art.svg'
            if f.exists():
                f.unlink()
        self.store.after_put = delete
        with self.assertRaises((u.Unsafe, OSError)):
            u.backup(self.c, self.store)
        self.no_checkpoint()
    def test_added_file_blocks_checkpoint(self):
        self.store.after_put = lambda _: (self.src / 'new.txt').write_text('new')
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.no_checkpoint()
    def test_permission_change_fails_closed(self):
        self.store.after_put = lambda _: (self.src / 'index.html').chmod(0)
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.no_checkpoint()
    def test_secret_names_and_archives_excluded(self):
        for name in ('.env.production', 'credentials.json', 'token-secret.txt', 'bundle.zip'):
            (self.src / name).write_bytes(b'dummy')
        m, _ = u.snapshot(self.c)
        self.assertEqual(len(m['files']), 2)
        self.assertEqual(len(m['excluded']), 4)
    def test_secret_content_stops_all_uploads(self):
        (self.src / 'innocent.js').write_bytes(b'const password = "' + b'a'*20 + b'";')
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.assertFalse(self.store.events)
    def test_presigned_url_content_stops_uploads(self):
        (self.src / 'evidence.json').write_text('{"url":"https://example.invalid?X-Amz-Signature=abc"}')
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_symlinks_rejected(self):
        (self.src / 'link.txt').symlink_to(self.src / 'art.svg')
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_symlink_ancestor_rejected(self):
        link = self.base / 'linked'
        link.symlink_to(self.src, target_is_directory=True)
        self.c['roots']['map'] = str(link)
        with self.assertRaises(OSError):
            u.snapshot(self.c)
    def test_hardlinks_rejected(self):
        os.link(self.src / 'art.svg', self.src / 'hard.svg')
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_budget_stops_before_upload(self):
        self.c['max_total_bytes'] = 1
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.assertFalse(self.store.events)
    def test_existing_restore_destination_preserved(self):
        r = u.backup(self.c, self.store)
        dest = self.base / 'restore'
        dest.mkdir()
        (dest / 'keep').write_text('original')
        with self.assertRaises(FileExistsError):
            u.restore(self.c, self.store, r['checkpoint'], dest)
        self.assertEqual((dest / 'keep').read_text(), 'original')
    def test_restore_corruption_fails(self):
        r = u.backup(self.c, self.store)
        self.store.corrupt = 'objects/'
        with self.assertRaises(u.Unsafe):
            u.restore(self.c, self.store, r['checkpoint'], self.base / 'restore')
    def test_checkpoint_tamper_fails_before_directory_creation(self):
        r = u.backup(self.c, self.store)
        self.store.corrupt = 'checkpoints/'
        with self.assertRaises(u.Unsafe):
            u.restore(self.c, self.store, r['checkpoint'], self.base / 'restore')
        self.assertFalse((self.base / 'restore').exists())
    def test_manifest_paths_duplicates_and_collisions(self):
        m, _ = u.snapshot(self.c)
        for path in ('../escape', '/absolute', 'map/../escape', 'map//file', 'map/./file', 'map\\file', 'map/C:foo'):
            altered = copy.deepcopy(m)
            altered['files'][0]['path'] = path
            with self.subTest(path=path), self.assertRaises(u.Unsafe):
                u.parse_manifest(u.encode(altered), self.c)
        m['files'].append(m['files'][0])
        with self.assertRaises(u.Unsafe):
            u.parse_manifest(u.encode(m), self.c)
        m, _ = u.snapshot(self.c)
        m['files'][0]['path'] = 'map/a'
        m['files'][1]['path'] = 'map/a/b'
        with self.assertRaises(u.Unsafe):
            u.parse_manifest(u.encode(m), self.c)
    def test_duplicate_json_keys_rejected(self):
        with self.assertRaises(u.Unsafe):
            u.decode(b'{"x":1,"x":2}')
    def test_missing_source_root(self):
        self.c['roots']['missing'] = str(self.base / 'missing')
        with self.assertRaises(FileNotFoundError):
            u.backup(self.c, self.store)
        self.assertFalse(self.store.events)

class AdditionalSafetyTests(unittest.TestCase):
    setUp = BackupTests.setUp
    def test_manifest_size_cap_before_any_upload(self):
        with patch.object(u, 'MANIFEST_LIMIT', 10):
            with self.assertRaises(u.Unsafe):
                u.backup(self.c, self.store)
        self.assertFalse(self.store.events)
    def test_additional_secret_shapes(self):
        for content in (b'{"api_token":"abcdefghijklmnopqrst"}', b'{"secret_key":"abcdefghijklmnopqrst"}', b'{"token":"abcdefghijklmnopqrst"}', b'postgres://user:password@example.invalid/db'):
            with self.subTest(content_type=content[:12]):
                self.assertIsNotNone(u.SECRET.search(content))
    def test_incremental_budget_before_any_put(self):
        self.c['max_new_bytes'] = 1
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.assertFalse(any(e[0] == 'put' for e in self.store.events))
    def test_upload_operation_budget_before_any_put(self):
        self.c['max_upload_operations'] = 1
        with self.assertRaises(u.Unsafe):
            u.backup(self.c, self.store)
        self.assertFalse(any(e[0] == 'put' for e in self.store.events))
    def test_safe_token_expressions_not_secrets(self):
        for data in (b'const matrixAccessToken = get(matrixAccessTokenStore);', b'const authToken = localUserStore.getAuthToken();', b'getOauthRefreshToken: getOauthRefreshToken(this.connection),', b'userRoomToken: this.connection ? this.connection.userRoomToken : ""'):
            self.assertIsNone(u.SECRET.search(data))
    def test_literal_tokens_remain_detected(self):
        for data in (b'const authToken = "abcdefghijklmnopqrst";', b'{"matrixAccessToken":"abcdefghijklmnopqrst"}', b'api_token: abcdefghijklmnopqrst', b'-----BEGIN PRIVATE KEY-----'):
            self.assertIsNotNone(u.SECRET.search(data))
    def test_chunked_roundtrip_and_duplicate_chunks(self):
        (self.src / 'large.bin').write_bytes(b'12345678'*5+b'last')
        with patch.object(u, 'CHUNK_BYTES', 8):
            r = u.backup(self.c, self.store)
            manifest_key = 'manifests/sha256/' + r['manifest']
            manifest = u.decode(self.store.objects[manifest_key])
            entry = next(e for e in manifest['files'] if e['path'].endswith('large.bin'))
            self.assertEqual(len(entry['chunks']), 6)
            self.assertEqual(len({x['sha256'] for x in entry['chunks']}), 2)
            u.restore(self.c, self.store, r['checkpoint'], self.base / 'restore')
        self.assertEqual((self.base/'restore/map/large.bin').read_bytes(), (self.src/'large.bin').read_bytes())
    def test_empty_file_roundtrip(self):
        (self.src/'empty.txt').write_bytes(b'')
        r = u.backup(self.c, self.store)
        u.restore(self.c,self.store,r['checkpoint'],self.base/'restore')
        self.assertEqual((self.base/'restore/map/empty.txt').read_bytes(), b'')
    def test_secret_crosses_chunk_boundary(self):
        (self.src/'bad.js').write_bytes(b'xxx password = "abcdefghijklmnopqrst"')
        with patch.object(u, 'CHUNK_BYTES', 8):
            with self.assertRaises(u.Unsafe):
                u.snapshot(self.c)
    def test_chunk_manifest_size_mismatch_rejected(self):
        m, _ = u.snapshot(self.c)
        m['files'][0]['chunks'][0]['size'] += 1
        with self.assertRaises(u.Unsafe):
            u.parse_manifest(u.encode(m), self.c)
    def test_missing_after_head_does_not_create(self):
        r = u.backup(self.c, self.store)
        original = self.store.exists
        def missing_after_head(key):
            answer = original(key)
            if key.startswith('objects/'):
                self.store.objects.pop(key, None)
            return answer
        self.store.exists = missing_after_head
        self.store.events = []
        with self.assertRaises(KeyError):
            u.backup(self.c, self.store)
        self.assertFalse(any(e[0] == 'put' for e in self.store.events))
    def test_aws_and_multiline_secret_assignments(self):
        for data in (b'aws_secret_access_key = "abcdefghijklmnopqrst"', b'aws_secret_access_key = abcdefghijklmnopqrst', b'{"password":\n "abcdefghijklmnopqrst"}', b'api_token: abcdefghijklmnopqrst\r\n'):
            self.assertIsNotNone(u.SECRET.search(data))
    def test_exact_hash_reviewed_file_inclusion(self):
        (self.src/'document.pdf').write_bytes(b'%PDF-fixture')
        self.c['reviewed_include']={'map/document.pdf':u.digest(b'%PDF-fixture')}
        m,_=u.snapshot(self.c)
        self.assertIn('map/document.pdf', [e['path'] for e in m['files']])
        (self.src/'document.pdf').write_bytes(b'%PDF-changed')
        with self.assertRaises(u.Unsafe):
            u.backup(self.c,self.store)
        self.assertFalse(self.store.events)
    def test_reviewed_include_never_waives_secret_scan(self):
        data=b'password = "abcdefghijklmnopqrst"'
        (self.src/'custom.unknown').write_bytes(data)
        self.c['reviewed_include']={'map/custom.unknown':u.digest(data)}
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_missing_reviewed_include_fails_closed(self):
        self.c['reviewed_include']={'map/gone.pdf':u.digest(b'%PDF-fixture')}
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_reviewed_include_cannot_admit_zip(self):
        data=b'PK\x03\x04fixture'
        (self.src/'bundle.zip').write_bytes(data)
        self.c['reviewed_include']={'map/bundle.zip':u.digest(data)}
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_disguised_archive_rejected(self):
        (self.src/'data.bin').write_bytes(b'PK\x03\x04fixture')
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_separate_reviewed_gzip_exact_hash(self):
        data=gzip.compress(b'nonsensitive fixture')
        (self.src/'proof.f64.gz').write_bytes(data)
        self.c['reviewed_gzip']={'map/proof.f64.gz':u.digest(data)}
        m,_=u.snapshot(self.c)
        self.assertIn('map/proof.f64.gz',[e['path'] for e in m['files']])
        (self.src/'proof.f64.gz').write_bytes(gzip.compress(b'changed'))
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_explicit_exclusion_dominates_review(self):
        (self.src/'paper.pdf').write_bytes(b'%PDF')
        self.c['reviewed_include']={'map/paper.pdf':u.digest(b'%PDF')}
        self.c['extra_exclude']=['map/paper.pdf']
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_root_files_selects_only_named_file(self):
        self.c['root_files']={'map':['art.svg']}
        m,_=u.snapshot(self.c)
        self.assertEqual([e['path'] for e in m['files']],['map/art.svg'])
        self.assertNotIn('map/index.html',m['excluded'])
    def fixture_review(self,data):
        return {'sha256':u.digest(data),'matches':[{'offset':m.start(),'length':m.end()-m.start(),'match_sha256':u.digest(m.group())} for m in u.SECRET.finditer(data)]}
    def test_exact_reviewed_synthetic_span(self):
        data=b'password = "abcdefghijklmnopqrst"'
        (self.src/'test.js').write_bytes(data)
        self.c['reviewed_nonsecret_matches']={'map/test.js':self.fixture_review(data)}
        u.snapshot(self.c)
        (self.src/'test.js').write_bytes(data+b' changed')
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_reviewed_fixture_rejects_extra_same_chunk_match(self):
        data=b'password = "abcdefghijklmnopqrst"'
        extra=data+b'; api_token = "zyxwvutsrqponmlkjihgf"'
        review=self.fixture_review(data)
        review['sha256']=u.digest(extra)
        (self.src/'test.js').write_bytes(extra)
        self.c['reviewed_nonsecret_matches']={'map/test.js':review}
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_fixture_match_wrong_span_rejected(self):
        data=b'password = "abcdefghijklmnopqrst"'
        review=self.fixture_review(data)
        review['matches'][0]['offset']+=1
        (self.src/'test.js').write_bytes(data)
        self.c['reviewed_nonsecret_matches']={'map/test.js':review}
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_reviewed_fixture_match_across_boundary(self):
        data=b'password = "abcdefghijklmnopqrstuvwx";'
        (self.src/'test.js').write_bytes(data)
        self.c['reviewed_nonsecret_matches']={'map/test.js':self.fixture_review(data)}
        with patch.object(u,'CHUNK_BYTES',28):
            u.snapshot(self.c)
    def test_conflicting_gzip_review_dictionaries_rejected(self):
        data=gzip.compress(b'fixture')
        (self.src/'proof.gz').write_bytes(data)
        self.c['reviewed_include']={'map/proof.gz':u.digest(data)}
        self.c['reviewed_gzip']={'map/proof.gz':u.digest(b'different')}
        with self.assertRaises(u.Unsafe):
            u.snapshot(self.c)
    def test_long_unreviewed_boundary_secret_rejected(self):
        (self.src/'bad.js').write_bytes(b'password = "'+b'A'*6000+b'"')
        with patch.object(u,'CHUNK_BYTES',6012):
            with self.assertRaises(u.Unsafe):
                u.snapshot(self.c)
    def test_oversize_reviewed_boundary_span_fails_closed(self):
        data=b'password = "'+b'A'*6000+b'"'
        (self.src/'test.js').write_bytes(data)
        self.c['reviewed_nonsecret_matches']={'map/test.js':self.fixture_review(data)}
        with patch.object(u,'CHUNK_BYTES',5500):
            with self.assertRaises(u.Unsafe):
                u.snapshot(self.c)
    def test_metadata_budget(self):
        with patch.object(u, 'METADATA_LIMIT', 1):
            with self.assertRaises(u.Unsafe):
                u.snapshot(self.c)
    def test_restore_syncs_directory_parents(self):
        nested = self.src / 'one/two'
        nested.mkdir(parents=True)
        (nested / 'deep.txt').write_text('deep')
        r = u.backup(self.c, self.store)
        calls = []
        original = os.fsync
        def sync(fd):
            calls.append(os.readlink('/proc/self/fd/' + str(fd)))
            original(fd)
        with patch.object(os, 'fsync', sync):
            u.restore(self.c, self.store, r['checkpoint'], self.base / 'restore')
        for path in (self.base, self.base / 'restore', self.base / 'restore/map', self.base / 'restore/map/one'):
            self.assertIn(str(path), calls)

class FakeClientError(Exception):
    def __init__(self, status):
        self.response = {'ResponseMetadata': {'HTTPStatusCode': status}}

class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.fake_exceptions = types.ModuleType('botocore.exceptions')
        self.fake_exceptions.ClientError = FakeClientError
        self.modules = patch.dict('sys.modules', {'botocore.exceptions': self.fake_exceptions})
        self.modules.start()
        self.addCleanup(self.modules.stop)
        self.store = u.R2Store.__new__(u.R2Store)
        self.store.bucket = 'test-bucket'
        self.store.prefix = 'v1/'
    def test_put_is_conditional(self):
        calls = []
        self.store.client = types.SimpleNamespace(put_object=lambda **kw: calls.append(kw))
        self.store.put_if_absent('objects/abc', b'data')
        self.assertEqual(calls[0]['IfNoneMatch'], '*')
        self.assertEqual(calls[0]['Key'], 'v1/objects/abc')
    def test_only_412_accepted_for_racing_put(self):
        for status in (403, 409, 412, 500):
            def fail(**kw):
                raise FakeClientError(status)
            self.store.client = types.SimpleNamespace(put_object=fail)
            if status == 412:
                self.store.put_if_absent('x', b'data')
            else:
                with self.assertRaises(FakeClientError):
                    self.store.put_if_absent('x', b'data')
    def test_head_only_404_means_absent(self):
        for status in (403, 404, 500):
            def fail(**kw):
                raise FakeClientError(status)
            self.store.client = types.SimpleNamespace(head_object=fail)
            if status == 404:
                self.assertFalse(self.store.exists('x'))
            else:
                with self.assertRaises(FakeClientError):
                    self.store.exists('x')
    def test_get_body_closed_on_oversize(self):
        stream = io.BytesIO(b'abcd')
        self.store.client = types.SimpleNamespace(get_object=lambda **kw: {'ContentLength': 4, 'Body': stream})
        with self.assertRaises(u.Unsafe):
            self.store.get('x', 3)
        self.assertTrue(stream.closed)
    def test_get_body_closed_on_read_failure(self):
        class Broken(io.BytesIO):
            def read(self, n):
                raise OSError('simulated')
        stream = Broken(b'abcd')
        self.store.client = types.SimpleNamespace(get_object=lambda **kw: {'ContentLength': 4, 'Body': stream})
        with self.assertRaises(OSError):
            self.store.get('x', 4)
        self.assertTrue(stream.closed)
    def test_sdk_without_condition_fails_before_write(self):
        client = types.SimpleNamespace(meta=types.SimpleNamespace(service_model=types.SimpleNamespace(operation_model=lambda n: types.SimpleNamespace(input_shape=types.SimpleNamespace(members={})))))
        fake_boto = types.ModuleType('boto3')
        fake_boto.client = lambda *a, **kw: client
        fake_config = types.ModuleType('botocore.config')
        fake_config.Config = lambda **kw: kw
        with patch.dict('sys.modules', {'boto3': fake_boto, 'botocore.config': fake_config}):
            with self.assertRaises(u.Unsafe):
                u.R2Store({'bucket': 'bucket', 'prefix': 'v1', 'account_id': '0'*32})

if __name__ == '__main__':
    unittest.main(verbosity=2)
