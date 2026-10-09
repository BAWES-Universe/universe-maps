"""Browser-host loopback QA server; bounded outputs only in runtime-work/results."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse, base64, binascii, json, os, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'runtime-work/results'
os.chdir(ROOT)

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path!='/qa/save':self.send_error(404);return
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=90_000_000:self.send_error(413);return
            payload=json.loads(self.rfile.read(length));name=payload['name']
            if not isinstance(name,str) or not re.fullmatch(r'[a-zA-Z0-9_-]{1,100}',name):raise ValueError('Invalid output name')
            kinds=[k for k in ('png','webm','report') if k in payload]
            if len(kinds)!=1:raise ValueError('Supply exactly one PNG, WebM or report')
            kind=kinds[0]
            if kind=='report':
                data=json.dumps(payload[kind],indent=2).encode();suffix='json'
                if len(data)>8_000_000:raise ValueError('Report exceeds 8 MB')
            else:
                prefix='data:image/png;base64,' if kind=='png' else 'data:video/webm;base64,'
                if not payload[kind].startswith(prefix):raise ValueError('Invalid media type')
                data=base64.b64decode(payload[kind][len(prefix):],validate=True);suffix=kind
                magic=b'\x89PNG\r\n\x1a\n' if kind=='png' else b'\x1aE\xdf\xa3'
                if not data.startswith(magic) or not 0<len(data)<=64_000_000:raise ValueError('Invalid media size/signature')
            OUT.mkdir(parents=True,exist_ok=True);path=OUT/f'{name}.{suffix}';path.write_bytes(data)
            reply=json.dumps({'saved':str(path.relative_to(ROOT)),'bytes':len(data)}).encode()
            self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(reply)));self.end_headers();self.wfile.write(reply)
        except (ValueError,KeyError,TypeError,binascii.Error) as error:self.send_error(400,str(error))
    def end_headers(self):
        self.send_header('Cache-Control','no-store');super().end_headers()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8846);args=parser.parse_args()
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
