"""Safe, offline URL heuristics. Never fetches, opens or resolves a URL."""
import re
from urllib.parse import urlsplit

MAX_URL_LEN = 2048
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy",
              "t.ly", "shorturl.at", "ow.ly", "tiny.cc", "rebrand.ly"}
RISKY_TLDS = {"xyz", "top", "click", "icu", "vip", "buzz", "loan", "work", "site", "cfd", "sbs"}
# brand token -> official registrable domain (verify before relying on this list)
BRANDS = {"sebi": "sebi.gov.in", "rbi": "rbi.org.in", "nseindia": "nseindia.com",
          "bseindia": "bseindia.com", "npci": "npci.org.in", "cybercrime": "cybercrime.gov.in"}

# indicator id -> (weight, label_en, label_hi, explain_en, explain_hi)
T = {
 "ip_host": (3, "Raw IP address as host", "होस्ट की जगह IP पता",
   "The link uses a numeric IP address instead of a normal website name, which is unusual for genuine financial services.",
   "लिंक में सामान्य वेबसाइट नाम की जगह IP संख्या है, जो असली वित्तीय सेवाओं में असामान्य है।"),
 "lookalike": (3, "Name resembles an official body", "नाम किसी सरकारी/नियामक संस्था जैसा दिखता है",
   "The address contains or closely resembles the name of a financial regulator or exchange but is not that body's official domain.",
   "पते में किसी नियामक/एक्सचेंज का नाम या उससे मिलता-जुलता नाम है, पर यह उनका आधिकारिक डोमेन नहीं है।"),
 "shortener": (2, "Shortened link", "छोटा किया गया लिंक",
   "Link shorteners hide the real destination. You cannot tell where it leads without opening it.",
   "छोटे लिंक असली पता छुपा देते हैं। खोले बिना पता नहीं चलता कि वह कहाँ जाता है।"),
 "no_https": (1, "No HTTPS", "HTTPS नहीं है",
   "The link does not use HTTPS, so traffic is not encrypted. (HTTPS alone does not prove a site is genuine.)",
   "लिंक HTTPS का उपयोग नहीं करता। (केवल HTTPS होना साइट के असली होने का प्रमाण नहीं है।)"),
 "punycode": (2, "Look-alike characters (punycode)", "मिलते-जुलते अक्षर (punycode)",
   "The address uses encoded international characters, sometimes used to imitate well-known names.",
   "पते में एन्कोडेड अंतरराष्ट्रीय अक्षर हैं, जो कभी-कभी जाने-माने नामों की नकल के लिए उपयोग होते हैं।"),
 "risky_tld": (1, "Domain ending often seen in throwaway sites", "ऐसा डोमेन अंत जो अक्सर अस्थायी साइटों में दिखता है",
   "This domain ending is cheap and common in short-lived sites. Many genuine sites exist on it too, so this is a weak signal.",
   "यह डोमेन अंत सस्ता है और अस्थायी साइटों में आम है। इस पर कई असली साइटें भी होती हैं, इसलिए यह कमज़ोर संकेत है।"),
 "userinfo": (3, "'@' inside the address", "पते में '@'",
   "Text before '@' is ignored by browsers and is used to disguise the real destination.",
   "'@' से पहले का हिस्सा ब्राउज़र अनदेखा करता है और असली गंतव्य छुपाने में प्रयोग होता है।"),
 "many_hyphens": (1, "Unusually many hyphens/subdomains", "बहुत सारे हाइफ़न/सबडोमेन",
   "Long, hyphen-heavy or deeply nested addresses are a common way to make a fake address look official.",
   "लंबे, हाइफ़न-भरे या बहुत सबडोमेन वाले पते नकली पते को असली दिखाने का आम तरीका हैं।"),
}
LEVELS = [(5, "high"), (3, "medium"), (1, "low"), (0, "none")]


def _lev1(a, b):
    """True if edit distance between a and b is exactly 1."""
    if a == b or abs(len(a) - len(b)) > 1:
        return False
    i = j = d = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1; j += 1; continue
        d += 1
        if d > 1:
            return False
        if len(a) > len(b): i += 1
        elif len(a) < len(b): j += 1
        else: i += 1; j += 1
    return d + (len(a) - i) + (len(b) - j) == 1


def _official(host, domain):
    return host == domain or host.endswith("." + domain)


def check_url(raw):
    """Returns dict(ok, error?, normalized, host, indicators=[(id, evidence)], score, level)."""
    if not isinstance(raw, str) or not raw.strip():
        return {"ok": False, "error": "empty"}
    raw = raw.strip()
    if len(raw) > MAX_URL_LEN or re.search(r"[\x00-\x1f\s]", raw):
        return {"ok": False, "error": "invalid"}
    if re.match(r"^(javascript|data|file|vbscript|ftp):", raw, re.I):
        return {"ok": False, "error": "scheme"}
    has_scheme = re.match(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://", raw)
    if has_scheme and not re.match(r"^https?://", raw, re.I):
        return {"ok": False, "error": "scheme"}
    candidate = raw if has_scheme else "http://" + raw
    try:
        parts = urlsplit(candidate)
        host = (parts.hostname or "").lower().rstrip(".")
    except ValueError:
        return {"ok": False, "error": "invalid"}
    if not host or ("." not in host and not re.match(r"^\d+$", host)):
        return {"ok": False, "error": "invalid"}
    found = []
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host) or re.fullmatch(r"(0x[0-9a-f]+|\d{8,10})", host):
        found.append(("ip_host", host))
    if "@" in parts.netloc:
        found.append(("userinfo", parts.netloc.split("@")[0] + "@"))
    if host in SHORTENERS:
        found.append(("shortener", host))
    if has_scheme and parts.scheme == "http":
        found.append(("no_https", "http://"))
    if "xn--" in host:
        found.append(("punycode", host))
    labels = host.split(".")
    if labels[-1] in RISKY_TLDS:
        found.append(("risky_tld", "." + labels[-1]))
    if host.count("-") >= 3 or len(labels) >= 5:
        found.append(("many_hyphens", host))
    for brand, domain in BRANDS.items():
        if _official(host, domain):
            continue
        tokens = re.split(r"[.\-]", host)
        if brand in tokens or any(brand in t and len(brand) >= 6 for t in tokens) \
           or any(len(brand) >= 6 and _lev1(t, brand) for t in tokens):
            found.append(("lookalike", host))
            break
    score = sum(T[i][0] for i, _ in found)
    level = next(l for t, l in LEVELS if score >= t)
    return {"ok": True, "normalized": candidate, "host": host, "indicators": found,
            "score": score, "level": level, "had_scheme": bool(has_scheme)}
