"""FastAPI wiring tests. Skipped automatically if fastapi/httpx are not installed (they were NOT in the build sandbox)."""
import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
try:
    from fastapi.testclient import TestClient
    from app.main import app
except Exception:  # pragma: no cover
    TestClient = None


@unittest.skipIf(TestClient is None, "fastapi/httpx not installed")
class FastApiTests(unittest.TestCase):
    def setUp(self): self.c = TestClient(app)

    def test_health_and_message(self):
        self.assertEqual(self.c.get("/api/health").status_code, 200)
        r = self.c.post("/api/analyze/message", json={"text": "Guaranteed returns, risk-free! Share your OTP now.", "language": "en"})
        self.assertEqual(r.status_code, 200); self.assertIn("evidence", r.json())

    def test_malformed(self):
        self.assertEqual(self.c.post("/api/analyze/message", content=b"nope", headers={"content-type": "application/json"}).status_code, 400)
        self.assertEqual(self.c.post("/api/analyze/image", content=b"x", headers={"content-type": "text/plain"}).status_code, 415)


if __name__ == "__main__":
    unittest.main()
