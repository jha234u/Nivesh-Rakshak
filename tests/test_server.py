"""Live end-to-end test of the zero-dependency server over real HTTP."""
import json, sys, threading, unittest, urllib.request, urllib.error
from http.server import ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
import run_stdlib
from app import service
from app.ratelimit import RateLimiter


class LiveServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service.LIMITER = RateLimiter(limit=1000)
        cls.srv = ThreadingHTTPServer(("127.0.0.1", 0), run_stdlib.H)
        cls.base = f"http://127.0.0.1:{cls.srv.server_address[1]}"
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls): cls.srv.shutdown()

    def req(self, path, data=None, ctype="application/json"):
        r = urllib.request.Request(self.base + path, data=data, headers={"Content-Type": ctype} if data is not None else {})
        try:
            with urllib.request.urlopen(r) as resp: return resp.status, resp.read(), resp.headers
        except urllib.error.HTTPError as e: return e.code, e.read(), e.headers

    def test_frontend_served_with_security_headers(self):
        s, body, h = self.req("/")
        self.assertEqual(s, 200); self.assertIn(b"NiveshRakshak", body)
        self.assertEqual(h["X-Content-Type-Options"], "nosniff"); self.assertIn("script-src 'self'", h["Content-Security-Policy"])
        self.assertEqual(self.req("/app.js")[0], 200); self.assertEqual(self.req("/style.css")[0], 200)

    def test_no_path_traversal(self):
        self.assertEqual(self.req("/../backend/run_stdlib.py")[0], 404)
        self.assertEqual(self.req("/%2e%2e/backend/run_stdlib.py")[0], 404)

    def test_message_api_hindi(self):
        s, body, _ = self.req("/api/analyze/message", json.dumps({"text": "गारंटीशुदा रिटर्न! अपना ओटीपी बताएं।", "language": "hi"}).encode())
        j = json.loads(body); self.assertEqual(s, 200); self.assertEqual(j["language"], "hi"); self.assertEqual(j["result_category"], "high_concern")

    def test_bad_inputs_over_http(self):
        self.assertEqual(self.req("/api/analyze/message", b"garbage")[0], 400)
        self.assertEqual(self.req("/api/analyze/image", b"hello", "text/plain")[0], 415)
        self.assertEqual(self.req("/api/resources")[0], 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
