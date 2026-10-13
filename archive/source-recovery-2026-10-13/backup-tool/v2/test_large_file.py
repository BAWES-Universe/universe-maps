"""Local disk-only >64MiB fixture; no R2, credentials or network requests."""
import hashlib
import json
import resource
import tempfile
from pathlib import Path
import universe_backup as u

class DiskFixtureStore:
    def __init__(self, root):
        self.root = root
        self.puts = 0
    def exists(self, key):
        return (self.root / key).exists()
    def put_if_absent(self, key, data):
        p = self.root / key
        p.parent.mkdir(parents=True, exist_ok=True)
        try:
            with p.open('xb') as f:
                f.write(data)
            self.puts += 1
        except FileExistsError:
            pass
    def get(self, key, limit):
        with (self.root / key).open('rb') as f:
            data = f.read(limit + 1)
        if len(data) > limit:
            raise u.Unsafe('oversize fixture object')
        return data

def run():
    with tempfile.TemporaryDirectory(prefix='universe-chunk-proof-') as d:
        base = Path(d)
        src = base / 'source'
        src.mkdir()
        p = src / 'large-artwork.bin'
        block = b'\0' * (1024 * 1024)
        expected = hashlib.sha256()
        with p.open('wb') as f:
            for i in range(101):
                f.write(block)
                expected.update(block)
        c = {'roots': {'large': str(src)}, 'max_total_bytes': 6*1024**3, 'max_file_bytes': 1024**3, 'max_files': 20000, 'max_new_bytes': 128*1024**2, 'max_upload_operations': 6000, 'extra_exclude': []}
        store = DiskFixtureStore(base/'mock-store')
        result = u.backup(c,store)
        manifest = u.decode(store.get('manifests/sha256/'+result['manifest'],u.MANIFEST_LIMIT))
        e = manifest['files'][0]
        assert e['size'] == 101*1024**2 and len(e['chunks']) == 13
        assert e['sha256'] == expected.hexdigest()
        target = base/'restored'
        r = u.restore(c,store,result['checkpoint'],target)
        assert r['verified'] and (target/'large/large-artwork.bin').stat().st_size == 101*1024**2
        again = u.backup(c,store)
        assert again['checkpoint'] == result['checkpoint'] and again['new_bytes'] == 0
        report = {'fixture_bytes':e['size'],'chunks':len(e['chunks']),'unique_chunk_objects':result['unique_objects'],'whole_file_sha256':e['sha256'],'clean_restore_verified':True,'idempotent_retry_verified':True,'network_requests':0,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'configured_inventory_limit_bytes':c['max_total_bytes'],'configured_upload_budget_bytes':c['max_new_bytes']}
        print(json.dumps(report,indent=2))

if __name__ == '__main__':
    run()
