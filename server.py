"""LAYAN — Scam Jammer demo server. Stdlib only. Run: python server.py"""
import json
import os
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

from engine import ARCHETYPES, Fleet

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8130
FLEET = Fleet()
LOCK = threading.Lock()


class Handler(SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def _send(self, status, obj):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        try:
            with LOCK:
                if path == "/api/archetypes":
                    return self._send(200, {k: {"label": v["label"], "fingerprint": v["fingerprint"]}
                                            for k, v in ARCHETYPES.items()})
                if path == "/api/stats":
                    return self._send(200, FLEET.stats())
                if path.startswith("/api/session/"):
                    parts = path.split("/")
                    sid = parts[3]
                    s = FLEET.sessions.get(sid)
                    if not s:
                        return self._send(404, {"error": "no such session"})
                    if len(parts) == 5 and parts[4] == "report":
                        return self._send(200, s.report())
                    return self._send(200, s.snapshot())
                if path == "/api/sessions":
                    return self._send(200, {sid: s.snapshot() for sid, s in FLEET.sessions.items()})
            return super().do_GET()
        except Exception as e:  # noqa: BLE001
            return self._send(500, {"error": str(e)})

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(n) or b"{}") if n else {}
            with LOCK:
                if path == "/api/start":
                    arch = body.get("archetype", "poslaju")
                    if arch not in ARCHETYPES:
                        return self._send(400, {"error": "unknown archetype"})
                    sid, s = FLEET.new(arch, seed=body.get("seed"))
                    return self._send(201, {"id": sid, **s.step(), **s.snapshot()})
                if path.startswith("/api/step/"):
                    sid = path.rsplit("/", 1)[-1]
                    s = FLEET.sessions.get(sid)
                    if not s:
                        return self._send(404, {"error": "no such session"})
                    return self._send(200, {"id": sid, **s.step(), **s.snapshot()})
            return self._send(404, {"error": "not found"})
        except Exception as e:  # noqa: BLE001
            return self._send(500, {"error": str(e)})

    def log_message(self, fmt, *args):
        pass


if __name__ == "__main__":
    print(f"\n  LAYAN — Scam Jammer demo:  http://localhost:{PORT}\n")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
