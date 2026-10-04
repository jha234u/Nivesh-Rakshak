"""Screenshot OCR. Images are processed in memory only and never written to disk."""
import io
MAX_BYTES = 5 * 1024 * 1024
MAX_PIXELS = 25_000_000


def sniff(data):
    if data[:8] == b"\x89PNG\r\n\x1a\n": return "png"
    if data[:3] == b"\xff\xd8\xff": return "jpeg"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP": return "webp"
    return None


def extract_text(data):
    """Returns {'ok': bool, 'text': str, 'error': code|None}. Codes: too_large, bad_type, corrupt, ocr_unavailable, no_text."""
    if not data or len(data) > MAX_BYTES:
        return {"ok": False, "text": "", "error": "too_large" if data else "bad_type"}
    if not sniff(data):
        return {"ok": False, "text": "", "error": "bad_type"}
    try:
        from PIL import Image
        import pytesseract
    except ImportError:
        return {"ok": False, "text": "", "error": "ocr_unavailable"}
    try:
        img = Image.open(io.BytesIO(data)); img.verify()
        img = Image.open(io.BytesIO(data))
        if img.width * img.height > MAX_PIXELS:
            return {"ok": False, "text": "", "error": "too_large"}
        img = img.convert("L")
    except Exception:
        return {"ok": False, "text": "", "error": "corrupt"}
    try:
        langs = "eng+hin" if "hin" in pytesseract.get_languages() else "eng"
        text = pytesseract.image_to_string(img, lang=langs, timeout=20).strip()
    except Exception:
        return {"ok": False, "text": "", "error": "ocr_unavailable"}
    return {"ok": bool(text), "text": text[:5000], "error": None if text else "no_text"}
