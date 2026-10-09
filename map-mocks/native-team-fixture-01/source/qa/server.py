"""Loopback-only QA server. Bounded PNG, JSON and WebM outputs in qa/results/."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse
import base64
import binascii
import json
import os
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qa' / 'results'
MAX_REQUEST = 90_000_000
MAX_MEDIA = 64_000_000
os.chdir(ROOT)


class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/qa/save':
            self.send_error(404)
            return
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= MAX_REQUEST:
                self.send_error(413)
                return
            payload = json.loads(self.rfile.read(length))
            name = payload['name']
            if not isinstance(name, str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}', name):
                raise ValueError('Invalid output name')
            media = [kind for kind in ('png', 'webm', 'report') if kind in payload]
            if len(media) != 1:
                raise ValueError('Provide exactly one PNG, WebM or report')
            kind = media[0]
            if kind == 'report':
                data = json.dumps(payload[kind], indent=2).encode()
                if len(data) > 2_000_000:
                    raise ValueError('Report exceeds 2 MB')
                suffix = 'json'
            else:
                encoded = payload[kind]
                prefix = 'data:image/png;base64,' if kind == 'png' else 'data:video/webm;base64,'
                if not isinstance(encoded, str) or not encoded.startswith(prefix):
                    raise ValueError('Invalid media data URL')
                data = base64.b64decode(encoded[len(prefix):], validate=True)
                if not 0 < len(data) <= MAX_MEDIA:
                    raise ValueError('Media exceeds 64 MB')
                magic = b'\x89PNG\r\n\x1a\n' if kind == 'png' else b'\x1aE\xdf\xa3'
                if not data.startswith(magic):
                    raise ValueError('Media signature does not match type')
                suffix = kind
            OUT.mkdir(exist_ok=True)
            destination = OUT / f'{name}.{suffix}'
            destination.write_bytes(data)
            result = json.dumps({'saved': f'qa/results/{destination.name}', 'bytes': len(data)}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(result)))
            self.end_headers()
            self.wfile.write(result)
        except (ValueError, KeyError, TypeError, binascii.Error) as error:
            self.send_error(400, str(error))

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8821)
    args = parser.parse_args()
    ThreadingHTTPServer(('127.0.0.1', args.port), Handler).serve_forever()
