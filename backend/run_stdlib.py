"""Zero-dependency server (Python 3.9+): serves the frontend and the same API as the FastAPI app.
Run:  python backend/run_stdlib.py [port]   ->  http://localhost:8000"""
import mimetypes, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from app import service

FRONTEND = Path(__file__).resolve().parents[1] / "frontend"
CSP = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:"


class H(BaseHTTPRequestHandler):
    server_version = "NiveshRakshak"

    def _send(self, status, body, ctype):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", CSP)
        self.end_headers()
        self.wfile.write(body)

    def _api(self, method):
        import json
        n = int(self.headers.get("Content-Length") or 0)
        if n > 5 * 1024 * 1024 + 1024:
            status, payload = service.error("too_large", status=413)
        else:
            body = self.rfile.read(n) if method == "POST" else b""
            status, payload = service.handle(method, self.path, body, self.headers.get("Content-Type", ""), self.client_address[0])
        self._send(status, json.dumps(payload, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_POST(self): self._api("POST")

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self._api("GET")
        rel = "index.html" if self.path.split("?")[0] in ("/", "") else self.path.split("?")[0].lstrip("/")
        f = (FRONTEND / rel).resolve()
        if FRONTEND.resolve() not in f.parents or not f.is_file():
            return self._send(404, b"Not found", "text/plain")
        self._send(200, f.read_bytes(), (mimetypes.guess_type(f.name)[0] or "application/octet-stream") + "; charset=utf-8" if f.suffix in (".html", ".js", ".css") else (mimetypes.guess_type(f.name)[0] or "application/octet-stream"))

    def log_message(self, *a): pass  # do not log request data


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"NiveshRakshak AI on http://localhost:{port}  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
