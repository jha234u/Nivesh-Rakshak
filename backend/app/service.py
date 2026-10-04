"""Framework-independent request handling, shared by the FastAPI app and the zero-dependency server."""
import json
from . import analyzer, assistant, ocr
from .resources import RESOURCES
from .ratelimit import RateLimiter

MAX_JSON = 20_000
LIMITER = RateLimiter()
ERR = {
 "rate": ("Too many requests. Please wait a minute.", "बहुत अधिक अनुरोध। कृपया एक मिनट प्रतीक्षा करें।"),
 "bad_json": ("Request body must be valid JSON.", "अनुरोध मान्य JSON होना चाहिए।"),
 "not_found": ("Not found.", "नहीं मिला।"),
 "too_large": ("Image is too large (max 5 MB).", "छवि बहुत बड़ी है (अधिकतम 5 MB)।"),
 "bad_type": ("Please upload a PNG, JPEG or WebP image.", "कृपया PNG, JPEG या WebP छवि अपलोड करें।"),
 "corrupt": ("This image could not be read.", "यह छवि पढ़ी नहीं जा सकी।"),
 "ocr_unavailable": ("Text extraction is not available on this server. Please paste the text into the message analyzer instead.", "इस सर्वर पर पाठ निकालना उपलब्ध नहीं है। कृपया पाठ संदेश विश्लेषक में चिपकाएँ।"),
 "no_text": ("No readable text was found. Try a clearer, larger screenshot or paste the text manually.", "कोई पढ़ने योग्य पाठ नहीं मिला। अधिक साफ़ स्क्रीनशॉट आज़माएँ या पाठ स्वयं चिपकाएँ।"),
 "server": ("Something went wrong. Nothing was stored.", "कुछ गलत हुआ। कुछ भी सहेजा नहीं गया।"),
}


def error(code, lang="en", status=400, detail=None):
    k = 1 if lang == "hi" else 0
    return status, {"status": "error", "error_code": code, "message": detail or ERR[code][k], "language": "hi" if k else "en"}


def _json(body):
    if len(body) > MAX_JSON:
        raise ValueError("too large")
    d = json.loads(body.decode("utf-8"))
    if not isinstance(d, dict):
        raise ValueError("object required")
    return d


def handle(method, path, body=b"", content_type="", client="anon"):
    """Returns (http_status, dict). Never raises."""
    try:
        path = path.split("?")[0].rstrip("/") or "/"
        if method == "GET" and path == "/api/health":
            return 200, {"status": "ok", "version": "0.1.0", "ocr": _ocr_ready(), "llm": "not_configured"}
        if method == "GET" and path == "/api/resources":
            return 200, {"status": "ok", "resources": RESOURCES,
                         "notice": "Not live-verified. Confirm each link/number on the official source before relying on it."}
        if method != "POST" or path not in ("/api/analyze/message", "/api/analyze/url", "/api/analyze/image", "/api/assistant/chat"):
            return error("not_found", status=404)
        if not LIMITER.allow(client):
            return error("rate", status=429)
        if path == "/api/analyze/image":
            lang = "hi" if "lang=hi" in content_type else "en"
            if not content_type.lower().startswith("image/"):
                return error("bad_type", lang, 415)
            res = ocr.extract_text(body)
            if res["error"] in ("too_large", "bad_type", "corrupt"):
                return error(res["error"], lang, 413 if res["error"] == "too_large" else 400)
            if res["error"] == "ocr_unavailable":
                return error("ocr_unavailable", lang, 503)
            if res["error"] == "no_text":
                return error("no_text", lang, 422)
            out = analyzer.analyze_message(res["text"], lang)
            out["extracted_text"] = res["text"]
            return 200, out
        try:
            d = _json(body)
        except Exception:
            return error("bad_json")
        lang = "hi" if d.get("language") == "hi" else "en"
        try:
            if path == "/api/analyze/message":
                return 200, analyzer.analyze_message(d.get("text"), lang)
            if path == "/api/analyze/url":
                return 200, analyzer.analyze_url(d.get("url"), lang)
            return 200, assistant.chat(d.get("message"), lang)
        except ValueError as e:
            return error("invalid_input", lang, 422, str(e))
    except Exception:
        return error("server", status=500)


def _ocr_ready():
    try:
        import pytesseract, PIL  # noqa
        return "available"
    except ImportError:
        return "unavailable"
