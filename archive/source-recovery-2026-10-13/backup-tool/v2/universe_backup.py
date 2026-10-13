#!/usr/bin/env python3
"""Bounded, append-only, content-addressed backup. No delete API exists here."""
import argparse
import fnmatch
import hashlib
import json
import logging
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

VERSION = 2
CHUNK_BYTES = 8 * 1024**2
MAX_SOURCE_BYTES = 1024**4
MANIFEST_LIMIT = 32 * 1024**2
METADATA_LIMIT = 8 * 1024**2
HEX = re.compile(r'^[0-9a-f]{64}$')
LABEL = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$')
EXCLUDE = ('.git', '.aws', '.ssh', '.codex', '.orbit-os', 'node_modules', '__pycache__',
           '.venv', 'venv', '.env*', '*secret*', '*credential*', '*.pem', '*.key',
           '*.p12', '*.pfx', '*.har', '*cookies*', '*session*', 'id_rsa*', 'id_ed25519*', '.npmrc', '.netrc', '.pypirc',
           '*.zip', '*.tar', '*.gz', '*.7z', '*.rar', '*.sqlite*', '*.db', '*.log',
           '*download*result*.json', '*download*input*.json', '*upload*.json')
EXTENSIONS = set('html htm css js mjs cjs jsx ts tsx json tmj tsj wam md txt svg png jpg jpeg webp gif ico avif woff woff2 ttf otf mp3 wav ogg mp4 webm glb gltf bin obj mtl py sh yaml yml toml xml csv'.split())
# Heuristics are deliberately conservative, not a guarantee that all secrets are found.
SECRET = re.compile(rb'(-----BEGIN [A-Z ]*PRIVATE KEY-----|'
                    rb'AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{20,}|'
                    rb'github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-)?[A-Za-z0-9_-]{24,}|'
                    rb'xox[baprs]-[A-Za-z0-9-]{12,}|'
                    rb'[?&](?:X-Amz-Signature|X-Amz-Credential|sig|token|access_token)=|'
                    rb'\b[a-z][a-z0-9+.-]{0,19}://[^\s/:@]{1,256}:[^\s/@]{1,256}@|'
                    rb'[\"\x27]?\b[A-Za-z0-9_-]{0,80}(?:token|password|secret(?:[_-]?key)?|secret[_-]?access[_-]?key|api[_-]?key)[\"\x27]?'
                    rb'\s*[:=]\s*[\"\x27][A-Za-z0-9_+/.=-]{12,}|'
                    rb'(?m:^[ \t]*\b[A-Za-z0-9_-]{0,80}(?:token|password|secret(?:[_-]?key)?|secret[_-]?access[_-]?key|api[_-]?key)'
                    rb'[ \t]*[:=][ \t]*[A-Za-z0-9_+/.=-]{12,}[ \t\r]*$))', re.I)

class Unsafe(Exception):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()

def decode(data):
    def unique(pairs):
        out = {}
        for key, value in pairs:
            if key in out:
                raise Unsafe('Duplicate JSON field')
            out[key] = value
        return out
    return json.loads(data, object_pairs_hook=unique)

def safe_path(value):
    if not isinstance(value, str) or not value or '\\' in value or ':' in value or any(ord(c) < 32 for c in value):
        raise Unsafe('Unsafe relative path')
    p = PurePosixPath(value)
    if p.is_absolute() or any(s in ('', '.', '..') for s in value.split('/')):
        raise Unsafe('Unsafe relative path')
    return p.parts

def checked_hash(value):
    if not isinstance(value, str) or not HEX.fullmatch(value):
        raise Unsafe('Invalid SHA256')
    return value

def signature(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)

def open_directory(path):
    # Never follow a symlink in any ancestor, including configured source roots.
    p = Path(os.path.abspath(path))
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in p.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise

def load_config(path):
    c = decode(Path(path).read_bytes())
    allowed = {'roots', 'max_total_bytes', 'max_file_bytes', 'max_files', 'extra_exclude', 'r2', 'max_new_bytes', 'max_upload_operations', 'reviewed_include', 'reviewed_gzip', 'root_files', 'reviewed_nonsecret_matches'}
    if set(c) - allowed:
        raise Unsafe('Unknown config field; credentials do not belong in config')
    if not isinstance(c.get('roots'), dict) or not c['roots']:
        raise Unsafe('At least one named source root is required')
    for name, value in c['roots'].items():
        if not LABEL.fullmatch(name) or not isinstance(value, str) or not Path(value).is_absolute():
            raise Unsafe('Invalid source root')
    for field, cap in [('max_total_bytes', MAX_SOURCE_BYTES), ('max_file_bytes', MAX_SOURCE_BYTES), ('max_files', 100000), ('max_new_bytes', MAX_SOURCE_BYTES), ('max_upload_operations', 300006)]:
        n = c.get(field)
        if type(n) is not int or not 0 < n <= cap:
            raise Unsafe('Explicit positive bounded byte/file limits required')
    if c['max_file_bytes'] > c['max_total_bytes']:
        raise Unsafe('File budget exceeds total budget')
    if not isinstance(c.get('extra_exclude', []), list) or not all(isinstance(x, str) for x in c.get('extra_exclude', [])):
        raise Unsafe('Invalid exclusions')
    if set(c.get('reviewed_include', {})) & set(c.get('reviewed_gzip', {})):
        raise Unsafe('Reviewed include and reviewed gzip scopes must not overlap')
    reviewed = c.get('reviewed_include', {})
    if not isinstance(reviewed, dict):
        raise Unsafe('Reviewed includes must be exact paths and SHA256 hashes')
    for key, sha in reviewed.items():
        parts = safe_path(key)
        if len(parts) < 2 or parts[0] not in c['roots']:
            raise Unsafe('Reviewed include is outside configured roots')
        checked_hash(sha)
    for key, sha in c.get('reviewed_gzip', {}).items():
        parts = safe_path(key)
        if len(parts) < 2 or parts[0] not in c['roots'] or not key.lower().endswith('.gz'):
            raise Unsafe('Reviewed gzip requires an exact .gz source file')
        checked_hash(sha)
    for root, paths in c.get('root_files', {}).items():
        if root not in c['roots'] or not isinstance(paths, list) or not paths:
            raise Unsafe('Invalid root file scope')
        for value in paths:
            safe_path(value)
    for key, review in c.get('reviewed_nonsecret_matches', {}).items():
        parts = safe_path(key)
        if len(parts) < 2 or parts[0] not in c['roots'] or set(review) != {'sha256', 'matches'}:
            raise Unsafe('Invalid nonsecret match review')
        checked_hash(review['sha256'])
        if not isinstance(review['matches'], list) or not review['matches']:
            raise Unsafe('Nonsecret review requires exact match spans')
        for match in review['matches']:
            if set(match) != {'offset', 'length', 'match_sha256'} or type(match['offset']) is not int or match['offset'] < 0 or type(match['length']) is not int or match['length'] < 1:
                raise Unsafe('Invalid nonsecret match span')
            checked_hash(match['match_sha256'])
    if 'r2' in c:
        r = c['r2']
        if not isinstance(r, dict) or set(r) != {'account_id', 'bucket', 'prefix'}:
            raise Unsafe('R2 requires only account_id, bucket and prefix')
        if not re.fullmatch('[a-f0-9]{32}', r['account_id']) or not re.fullmatch('[a-z0-9][a-z0-9-]{1,61}[a-z0-9]', r['bucket']):
            raise Unsafe('Invalid R2 account or bucket')
        safe_path(r['prefix'])
    return c

class BlobRef:
    def __init__(self, root, relative, offset, size, source_signature):
        self.root, self.relative, self.offset, self.size, self.source_signature = root, relative, offset, size, source_signature
    def __len__(self):
        return self.size
    def read(self):
        parts = safe_path(self.relative)
        fd = open_directory(self.root)
        try:
            for part in parts[:-1]:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
            f = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            with os.fdopen(f, 'rb') as stream:
                if signature(os.fstat(stream.fileno())) != self.source_signature:
                    raise Unsafe('Source changed before chunk upload')
                stream.seek(self.offset)
                data = stream.read(self.size)
                if len(data) != self.size or signature(os.fstat(stream.fileno())) != self.source_signature or signature(os.stat(parts[-1], dir_fd=fd, follow_symlinks=False)) != self.source_signature:
                    raise Unsafe('Source changed during chunk upload')
                return data
        finally:
            os.close(fd)

def snapshot(c, stats_only=False):
    if set(c.get('reviewed_include', {})) & set(c.get('reviewed_gzip', {})):
        raise Unsafe('Reviewed include and reviewed gzip scopes must not overlap')
    entries, blobs, skipped = [], {}, []
    total = 0
    metadata_bytes = 0
    def walk(fd, root_name, rel=''):
        nonlocal total, metadata_bytes
        before = os.fstat(fd)
        if not before.st_mode & 0o444 or not before.st_mode & 0o111:
            raise Unsafe('Unreadable source directory')
        for name in sorted(os.listdir(fd)):
            relative = rel + name
            key = root_name + '/' + relative
            selected = c.get('root_files', {}).get(root_name)
            if selected is not None and relative not in selected and not any(p.startswith(relative + '/') for p in selected):
                continue  # Unrelated siblings are outside scope, including their names.
            safe_path(key)
            metadata_bytes += len(key.encode('utf-8')) + 128
            if metadata_bytes > METADATA_LIMIT:
                raise Unsafe('Source path metadata exceeds bounded budget')
            if any(fnmatch.fnmatch(key, p) for p in c.get('extra_exclude', [])):
                skipped.append(key)
                continue
            reviewed = key in c.get('reviewed_include', {}) or key in c.get('reviewed_gzip', {})
            archive_suffix = Path(name).suffix.lower() in ('.zip', '.tar', '.gz', '.7z', '.rar')
            if reviewed and archive_suffix and key not in c.get('reviewed_gzip', {}):
                raise Unsafe('Raw archive cannot be admitted by reviewed_include')
            if not reviewed and any(fnmatch.fnmatch(name.lower(), p.lower()) for p in EXCLUDE):
                skipped.append(key)
                continue
            s = os.stat(name, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISLNK(s.st_mode):
                raise Unsafe('Source symlink rejected')
            if stat.S_ISDIR(s.st_mode):
                if reviewed:
                    raise Unsafe('Reviewed include must be a file, never a directory')
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                try:
                    if signature(os.fstat(child)) != signature(s):
                        raise Unsafe('Directory changed during scan')
                    walk(child, root_name, relative + '/')
                finally:
                    os.close(child)
                continue
            if not stat.S_ISREG(s.st_mode) or s.st_nlink != 1:
                raise Unsafe('Special or hard-linked source file rejected')
            if not reviewed and Path(name).suffix.lower().lstrip('.') not in EXTENSIONS and name not in ('Dockerfile', 'LICENSE', 'Makefile', '.gitignore'):
                skipped.append(key)
                continue
            if not s.st_mode & 0o444:
                raise Unsafe('Unreadable source file')
            if len(entries) >= c['max_files']:
                raise Unsafe('Source exceeds configured file-count budget')
            if stats_only:
                entries.append({'path': key, 'size': s.st_size})
                total += s.st_size
                continue
            if s.st_size > c['max_file_bytes'] or total + s.st_size > c['max_total_bytes']:
                raise Unsafe('Source exceeds configured budget')
            f = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            try:
                if signature(os.fstat(f)) != signature(s):
                    raise Unsafe('File changed before read')
                whole = hashlib.sha256()
                chunks = []
                offset = 0
                tail = b''
                fixture = c.get('reviewed_nonsecret_matches', {}).get(key)
                approved_spans = {(m['offset'], m['length'], m['match_sha256']) for m in fixture['matches']} if fixture else set()
                observed_spans = set()
                with os.fdopen(f, 'rb', closefd=False) as stream:
                    while True:
                        data = stream.read(CHUNK_BYTES)
                        if not data:
                            break
                        offset += len(data)
                        if offset > c['max_file_bytes'] or total + offset > c['max_total_bytes']:
                            raise Unsafe('Source grew beyond configured byte budget')
                        if offset == len(data):
                            is_zip = data.startswith((b'PK\x03\x04', b'PK\x05\x06', b'PK\x07\x08'))
                            is_gzip = data.startswith(b'\x1f\x8b')
                            is_other_archive = data.startswith((b'7z\xbc\xaf\x27\x1c', b'Rar!')) or data[257:262] == b'ustar'
                            if (is_zip and not (reviewed and name.lower().endswith('.xlsx'))) or (is_gzip and key not in c.get('reviewed_gzip', {})) or is_other_archive:
                                raise Unsafe('Unreviewed archive/container content rejected')
                        scan = tail + data
                        scan_offset = offset - len(data) - len(tail)
                        for match in SECRET.finditer(scan):
                            span = (scan_offset + match.start(), match.end()-match.start(), digest(match.group()))
                            if span not in approved_spans:
                                # Defer only a prefix of a specifically reviewed short span.
                                # Ordinary/unapproved matches always fail immediately.
                                pending_review = (offset < s.st_size and match.end() == len(scan)
                                                  and any(o == span[0] and span[1] < n <= 4096 for o, n, h in approved_spans))
                                if pending_review:
                                    continue
                                raise Unsafe('Potential secret pattern in source file ' + key + '; no checkpoint created. Review locally')
                            observed_spans.add(span)
                        tail = (tail + data)[-4096:]
                        whole.update(data)
                        h = digest(data)
                        chunks.append({'sha256': h, 'size': len(data)})
                        metadata_bytes += 128
                        if metadata_bytes > METADATA_LIMIT:
                            raise Unsafe('Chunk metadata exceeds bounded budget')
                        blobs.setdefault(h, BlobRef(c['roots'][root_name], relative, offset-len(data), len(data), signature(s)))
                if signature(os.fstat(f)) != signature(s) or signature(os.stat(name, dir_fd=fd, follow_symlinks=False)) != signature(s) or offset != s.st_size:
                    raise Unsafe('File changed during read')
            finally:
                os.close(f)
            expected_review_hash = c.get('reviewed_gzip', {}).get(key) or c.get('reviewed_include', {}).get(key)
            if reviewed and whole.hexdigest() != expected_review_hash:
                raise Unsafe('Reviewed include hash changed; new review required')
            if fixture and (whole.hexdigest() != fixture['sha256'] or observed_spans != approved_spans):
                raise Unsafe('Reviewed nonsecret source changed; new review required')
            entries.append({'path': key, 'sha256': whole.hexdigest(), 'size': offset, 'executable': bool(s.st_mode & 0o111), 'chunks': chunks})
            total += offset
        if signature(os.fstat(fd)) != signature(before):
            raise Unsafe('Directory changed during scan')
    for name, path in sorted(c['roots'].items()):
        fd = open_directory(path)
        try:
            walk(fd, name)
        finally:
            os.close(fd)
    required = set(c.get('reviewed_include', {})) | set(c.get('reviewed_gzip', {})) | set(c.get('reviewed_nonsecret_matches', {}))
    required |= {root + '/' + relative for root, paths in c.get('root_files', {}).items() for relative in paths}
    if not required.issubset({e['path'] for e in entries}):
        raise Unsafe('A reviewed include is missing or excluded by its parent directory')
    if not entries:
        raise Unsafe('No eligible files found')
    manifest = {'version': VERSION, 'files': entries, 'excluded': sorted(skipped)}
    return manifest, blobs

class R2Store:
    """Only HEAD/GET and conditional create; credentials use boto3's standard chain."""
    def __init__(self, config):
        import boto3
        from botocore.config import Config
        # No credential arguments, profiles embedded in config, URL signing or debug logs.
        logging.getLogger('boto3').setLevel(logging.CRITICAL)
        logging.getLogger('botocore').setLevel(logging.CRITICAL)
        self.bucket = config['bucket']
        self.prefix = config['prefix'] + '/'
        self.client = boto3.client('s3', endpoint_url='https://' + config['account_id'] + '.r2.cloudflarestorage.com', region_name='auto',
                                  config=Config(connect_timeout=10, read_timeout=60, retries={'total_max_attempts': 3, 'mode': 'standard'},
                                                request_checksum_calculation='when_required', response_checksum_validation='when_required'))
        # Fail before writing if installed SDK cannot enforce conditional creation.
        shape = self.client.meta.service_model.operation_model('PutObject').input_shape
        if 'IfNoneMatch' not in shape.members:
            raise Unsafe('Installed boto3 lacks conditional create support')
    def exists(self, key):
        from botocore.exceptions import ClientError
        try:
            self.client.head_object(Bucket=self.bucket, Key=self.prefix + key)
            return True
        except ClientError as e:
            if e.response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 404:
                return False
            raise
    def put_if_absent(self, key, data):
        from botocore.exceptions import ClientError
        try:
            self.client.put_object(Bucket=self.bucket, Key=self.prefix + key, Body=data, IfNoneMatch='*')
        except ClientError as e:
            if e.response.get('ResponseMetadata', {}).get('HTTPStatusCode') != 412:
                raise
    def get(self, key, limit):
        response = self.client.get_object(Bucket=self.bucket, Key=self.prefix + key)
        stream = response['Body']
        try:
            if response.get('ContentLength', limit + 1) > limit:
                raise Unsafe('Remote object exceeds expected size')
            data = stream.read(limit + 1)
            if len(data) > limit:
                raise Unsafe('Remote object exceeds expected size')
            return data
        finally:
            stream.close()

def ensure(store, key, data, may_create):
    if may_create:
        store.put_if_absent(key, data)
    # ETag/HEAD metadata is never treated as proof of backup integrity.
    fetched = store.get(key, len(data))
    if len(fetched) != len(data) or digest(fetched) != digest(data):
        raise Unsafe('Remote readback hash mismatch; no success claimed')

def backup(c, store, initial=None):
    manifest, blobs = initial or snapshot(c)
    raw = encode(manifest)
    if len(raw) > MANIFEST_LIMIT:
        raise Unsafe('Manifest exceeds restore limit; no upload made')
    mh = digest(raw)
    checkpoint = encode({'version': VERSION, 'manifest_sha256': mh, 'file_count': len(manifest['files'])})
    ch = digest(checkpoint)
    objects = [('objects/sha256/' + h, data) for h, data in sorted(blobs.items())]
    metadata = [('manifests/sha256/' + mh, raw), ('checkpoints/sha256/' + ch, checkpoint)]
    # Bound the full run BEFORE the first write, including metadata. A HEAD error fails closed.
    missing = {key for key, data in objects + metadata if not store.exists(key)}
    new_bytes = sum(len(data) for key, data in objects + metadata if key in missing)
    # SDK has total_max_attempts=3, so count a conservative maximum of three PUT attempts.
    upload_operations = len(missing) * 3
    if new_bytes > c['max_new_bytes'] or upload_operations > c['max_upload_operations']:
        raise Unsafe('Incremental upload exceeds configured new-byte/operation budget; no upload made')
    for key, reference in objects:
        data = reference.read()
        if digest(data) != key.rsplit('/', 1)[-1]:
            raise Unsafe('Source chunk hash changed before upload')
        ensure(store, key, data, key in missing)
    second, _ = snapshot(c)
    if second != manifest:
        raise Unsafe('Source changed during backup; no checkpoint created')
    for key, data in metadata:
        ensure(store, key, data, key in missing)
    return {'checkpoint': ch, 'manifest': mh, 'files': len(manifest['files']), 'unique_objects': len(blobs), 'new_bytes': new_bytes, 'maximum_put_attempts': upload_operations, 'verified_bytes': sum(map(len, blobs.values()))}

def parse_manifest(raw, c):
    m = decode(raw)
    if set(m) != {'version', 'files', 'excluded'} or m['version'] != VERSION or not isinstance(m['files'], list) or not isinstance(m['excluded'], list):
        raise Unsafe('Invalid manifest schema')
    if not 0 < len(m['files']) <= c['max_files']:
        raise Unsafe('Invalid manifest file count')
    seen, total = set(), 0
    for e in m['files']:
        if not isinstance(e, dict) or set(e) != {'path', 'sha256', 'size', 'executable', 'chunks'}:
            raise Unsafe('Invalid manifest entry')
        parts = safe_path(e['path'])
        checked_hash(e['sha256'])
        if len(parts) < 2 or not LABEL.fullmatch(parts[0]) or e['path'] in seen or type(e['size']) is not int or not 0 <= e['size'] <= c['max_file_bytes'] or type(e['executable']) is not bool:
            raise Unsafe('Invalid or duplicate manifest path/size')
        if not isinstance(e['chunks'], list):
            raise Unsafe('Invalid file chunks')
        chunk_total = 0
        for chunk_index, chunk in enumerate(e['chunks']):
            if not isinstance(chunk, dict) or set(chunk) != {'sha256', 'size'} or type(chunk['size']) is not int or not 0 < chunk['size'] <= CHUNK_BYTES:
                raise Unsafe('Invalid chunk schema/size')
            if chunk_index < len(e['chunks']) - 1 and chunk['size'] != CHUNK_BYTES:
                raise Unsafe('Non-final chunk has noncanonical size')
            checked_hash(chunk['sha256'])
            chunk_total += chunk['size']
        if chunk_total != e['size'] or (e['size'] == 0 and e['sha256'] != digest(b'')):
            raise Unsafe('Chunk/file size mismatch')
        seen.add(e['path'])
        total += e['size']
    if total > c['max_total_bytes']:
        raise Unsafe('Restore exceeds byte budget')
    for name in seen:
        if any('/'.join(name.split('/')[:i]) in seen for i in range(1, len(name.split('/')))):
            raise Unsafe('Manifest file/directory collision')
    return m

def restore(c, store, checkpoint_id, destination):
    checked_hash(checkpoint_id)
    cpraw = store.get('checkpoints/sha256/' + checkpoint_id, 4096)
    if digest(cpraw) != checkpoint_id:
        raise Unsafe('Checkpoint hash mismatch')
    cp = decode(cpraw)
    if set(cp) != {'version', 'manifest_sha256', 'file_count'} or cp['version'] != VERSION:
        raise Unsafe('Invalid checkpoint')
    mh = checked_hash(cp['manifest_sha256'])
    raw = store.get('manifests/sha256/' + mh, MANIFEST_LIMIT)
    if digest(raw) != mh:
        raise Unsafe('Manifest hash mismatch')
    m = parse_manifest(raw, c)
    if type(cp['file_count']) is not int or cp['file_count'] != len(m['files']):
        raise Unsafe('Checkpoint count mismatch')
    dest = Path(os.path.abspath(destination))
    pfd = open_directory(dest.parent)
    try:
        # Existing destination is always refused, even if empty. No merge/overwrite mode.
        os.mkdir(dest.name, 0o700, dir_fd=pfd)
        os.fsync(pfd)
        rootfd = os.open(dest.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=pfd)
    finally:
        os.close(pfd)
    try:
        for entry in m['files']:
            parts = safe_path(entry['path'])
            fd = os.dup(rootfd)
            try:
                for name in parts[:-1]:
                    try:
                        os.mkdir(name, 0o700, dir_fd=fd)
                        os.fsync(fd)
                    except FileExistsError:
                        pass
                    child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                    os.close(fd)
                    fd = child
                f = os.open(parts[-1], os.O_RDWR | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o700 if entry['executable'] else 0o600, dir_fd=fd)
                with os.fdopen(f, 'w+b') as stream:
                    whole = hashlib.sha256()
                    count = 0
                    for chunk in entry['chunks']:
                        data = store.get('objects/sha256/' + chunk['sha256'], chunk['size'])
                        if len(data) != chunk['size'] or digest(data) != chunk['sha256']:
                            raise Unsafe('Restore chunk hash mismatch; partial destination preserved')
                        stream.write(data)
                        whole.update(data)
                        count += len(data)
                    if count != entry['size'] or whole.hexdigest() != entry['sha256']:
                        raise Unsafe('Restore whole-file hash mismatch')
                    stream.flush()
                    os.fsync(stream.fileno())
                    stream.seek(0)
                    check = hashlib.sha256()
                    while True:
                        block = stream.read(CHUNK_BYTES)
                        if not block:
                            break
                        check.update(block)
                    if check.hexdigest() != entry['sha256']:
                        raise Unsafe('Restored file readback mismatch')
                os.fsync(fd)
            finally:
                os.close(fd)
        os.fsync(rootfd)
    finally:
        os.close(rootfd)
    return {'checkpoint': checkpoint_id, 'restored_files': len(m['files']), 'verified': True}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('preflight', help='Local-only scan; never accesses R2')
    b = sub.add_parser('backup', help='One bounded run; requires explicit write flag')
    b.add_argument('--enable-r2-writes', action='store_true')
    r = sub.add_parser('restore', help='Download and verify into a NEW directory')
    r.add_argument('--checkpoint', required=True)
    r.add_argument('--destination', required=True)
    args = p.parse_args()
    try:
        c = load_config(args.config)
        if args.command == 'preflight':
            inventory, _ = snapshot(c, stats_only=True)
            total = sum(e['size'] for e in inventory['files'])
            summary = {'mode': 'local-only dry run', 'eligible_files': len(inventory['files']), 'logical_bytes': total,
                       'largest_file_bytes': max(e['size'] for e in inventory['files']),
                       'excluded_count': len(inventory['excluded']), 'excluded_paths': inventory['excluded'],
                       'configured_max_new_bytes': c['max_new_bytes'], 'configured_max_upload_operations': c['max_upload_operations']}
            if total > c['max_total_bytes'] or summary['largest_file_bytes'] > c['max_file_bytes']:
                summary.update(status='budget_exceeded', unique_bytes=None, content_scan='not run: exceeds approved byte budget')
                print(json.dumps(summary, indent=2))
                return 1
            m, blobs = snapshot(c)
            if [(e['path'], e['size']) for e in inventory['files']] != [(e['path'], e['size']) for e in m['files']]:
                raise Unsafe('Source changed between inventory and content scan')
            summary.update(status='local_content_scan_passed', unique_bytes=sum(map(len, blobs.values())),
                           upper_bound_object_puts=len(blobs) + 2, upper_bound_put_attempts=3 * (len(blobs) + 2),
                           upper_bound_readback_bytes=sum(map(len, blobs.values())) + len(encode(m)) + 4096)
            print(json.dumps(summary, indent=2))
        else:
            if args.command == 'backup' and not args.enable_r2_writes:
                raise Unsafe('R2 write flag is required; no network request made')
            if 'r2' not in c:
                raise Unsafe('R2 is not configured')
            initial = snapshot(c) if args.command == 'backup' else None
            store = R2Store(c['r2'])
            result = backup(c, store, initial) if args.command == 'backup' else restore(c, store, args.checkpoint, args.destination)
            print(json.dumps(result, indent=2))
    except (Exception, KeyboardInterrupt) as error:
        # Never print SDK exceptions/tracebacks, request headers or signed URLs.
        print('Backup/restore stopped safely: ' + (str(error) if isinstance(error, Unsafe) else type(error).__name__) + '. No verified success claimed.', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
