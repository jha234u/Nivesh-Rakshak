"""Transparent rule-based message analysis. Evidence is always an exact substring of the input."""
import re
from . import urlcheck

MAX_TEXT_LEN = 5000
MIN_TEXT_LEN = 8
F = re.I | re.U

# id -> (weight, label_en, label_hi, explain_en, explain_hi, negatable, [patterns])
RULES = {
 "guaranteed_returns": (3, "Guaranteed or unusually high returns", "गारंटीशुदा या असामान्य रूप से ऊँचा रिटर्न",
   "Genuine investments cannot guarantee returns. Promises of assured, risk-free or very high profits are a classic warning sign.",
   "असली निवेश में रिटर्न की गारंटी नहीं दी जा सकती। पक्के, बिना-जोखिम या बहुत ऊँचे मुनाफ़े के वादे चेतावनी का आम संकेत हैं।", True, [
   r"guarantee[ds]?\s+(returns?|profits?|income)", r"assured\s+(returns?|profits?|income)",
   r"\b\d{3,}\s*%\s*(profit|returns?|guaranteed)", r"risk[- ]?free", r"double\s+(your\s+)?money",
   r"\b\d{1,3}\s*%\s*(daily|per\s+day|weekly|per\s+week|monthly|per\s+month)",
   r"गारंटी", r"पक्का\s*(मुनाफ़ा|मुनाफा|रिटर्न)", r"दोगुना", r"बिना\s*(किसी\s*)?(जोखिम|रिस्क)", r"रोज़?\s*\d+\s*%"]),
 "urgency": (1, "Artificial urgency or pressure", "बनावटी जल्दबाज़ी या दबाव",
   "Scammers push you to act before you can think or check. Genuine opportunities do not vanish in hours.",
   "ठग आपको सोचने या जाँचने से पहले कदम उठाने के लिए दबाव डालते हैं। असली अवसर घंटों में ग़ायब नहीं होते।", False, [
   r"hurry", r"last\s+chance", r"limited\s+(seats|slots|spots|time|period)", r"only\s+today", r"act\s+now",
   r"within\s+\d+\s*(hours?|minutes?|mins?)", r"offer\s+(expires|ends)", r"जल्दी", r"आज\s*ही", r"सीमित\s*(सीट|समय|स्थान)", r"आखिरी\s*मौका|आख़िरी\s*मौका"]),
 "sensitive_info": (3, "Request for OTP, password or personal/bank details", "OTP, पासवर्ड या निजी/बैंक जानकारी की माँग",
   "No genuine bank, broker or regulator asks you to share an OTP, password, PIN or card details by message or call.",
   "कोई असली बैंक, ब्रोकर या नियामक संदेश या कॉल पर OTP, पासवर्ड, PIN या कार्ड विवरण नहीं माँगता।", True, [
   r"(share|send|give|tell|provide|submit|forward|reply|confirm|update|verify|enter)\b[^.\n]{0,40}\b(otp|password|cvv|aadhaar|aadhar|pan\s*(card|number)?|card\s+number|bank\s+details|upi\s+pin|net\s*banking)",
   r"\b(otp|password|cvv|aadhaar|aadhar|card\s+number|bank\s+details|upi\s+pin)\b[^.\n]{0,30}\b(share|send|give|tell|provide|submit|forward|reply|confirm)",
   r"(ओटीपी|पासवर्ड|आधार|पैन|सीवीवी|खाता\s*नंबर)[^.\n।]{0,30}(बताएं|बताइए|बताओ|भेजें|भेजो|दें|साझा)",
   r"(बताएं|बताइए|भेजें|साझा|दें)[^.\n।]{0,30}(ओटीपी|पासवर्ड|आधार|पैन|सीवीवी|खाता\s*नंबर)"]),
 "impersonation": (2, "Possible impersonation of an official or institution", "किसी अधिकारी/संस्था का रूप धरने की संभावना",
   "The message claims to come from an official body or officer. Scammers often borrow trusted names.",
   "संदेश किसी सरकारी संस्था या अधिकारी की ओर से होने का दावा करता है। ठग अक्सर भरोसेमंद नामों का सहारा लेते हैं।", False, [
   r"\b(sebi|rbi|nse|bse|npci)\s+(official|officer|executive|representative|team|department)",
   r"(calling|message|messaging|writing)\s+from\s+(sebi|rbi|your\s+bank|the\s+bank|police|cyber\s*cell)",
   r"customer\s+(care|support)\s+(executive|manager)", r"(सेबी|आरबीआई|बैंक|पुलिस)\s*(के\s*)?(अधिकारी|से\s*बोल)"]),
 "regulatory_claim": (1, "Unverified claim of regulatory approval", "बिना सबूत नियामक मंज़ूरी का दावा",
   "The message claims approval or registration. Such claims are easy to make and must be checked on the official website.",
   "संदेश मंज़ूरी या पंजीकरण का दावा करता है। ऐसे दावे आसान हैं और इन्हें आधिकारिक वेबसाइट पर जाँचना ज़रूरी है।", False, [
   r"(sebi|rbi)[\s-]*(registered|approved|certified|authori[sz]ed)", r"(government|govt\.?)[\s-]*(approved|backed|scheme)",
   r"सेबी\s*(पंजीकृत|मान्यता|से\s*मान्य)", r"सरकार\s*(द्वारा\s*)?(मान्य|अनुमोदित)"]),
 "payment_request": (2, "Suspicious payment instruction or fee", "संदिग्ध भुगतान निर्देश या शुल्क",
   "Requests to send money to a personal UPI ID or QR code, or to pay a fee to unlock returns, are common in investment scams.",
   "व्यक्तिगत UPI ID/QR पर पैसे भेजने या रिटर्न पाने के लिए शुल्क देने की माँग निवेश ठगी में आम है।", False, [
   r"(send|transfer|pay|deposit)\s+(rs\.?|₹|inr)?\s*[\d,]{3,}", r"\b(registration|processing|activation|joining|release)\s+(fee|charges?)\b",
   r"\bupi\s*(id)?\s*[:\-]?\s*[\w.\-]+@\w+", r"scan\s+(the\s+)?qr", r"(शुल्क|फीस)\s*(जमा|भेजें|भरें)",
   r"(पैसे|रुपये|रकम)\s*(जमा|भेजें|ट्रांसफर)"]),
 "group_invite": (1, "Invitation to a private tips group", "निजी टिप्स ग्रुप का निमंत्रण",
   "Invitations to 'VIP' WhatsApp/Telegram groups are a common way to funnel people toward pump-and-dump or fake-platform schemes.",
   "'VIP' WhatsApp/Telegram ग्रुप के निमंत्रण लोगों को नकली प्लेटफ़ॉर्म या शेयर-उछाल ठगी की ओर ले जाने का आम तरीका हैं।", False, [
   r"(join|link)\s+(our|my|the)?\s*(vip|premium)?\s*(whatsapp|telegram)\s*(group|channel)", r"\bvip\s+(group|channel|members?)\b",
   r"(व्हाट्सएप|वॉट्सऐप|टेलीग्राम)\s*(ग्रुप|चैनल)"]),
 "tip_language": (2, "Insider / 'sure-shot' tip language", "इनसाइडर / 'पक्की' टिप की भाषा",
   "Phrases like 'sure-shot' or 'insider tip' imply certainty or secret knowledge that no honest adviser can offer.",
   "'सुनिश्चित', 'इनसाइडर टिप' जैसे शब्द ऐसी निश्चितता या गुप्त जानकारी जताते हैं जो कोई ईमानदार सलाहकार नहीं दे सकता।", False, [
   r"sure[- ]?shot", r"insider\s+(tip|info|news|information)", r"\bjackpot\b", r"operator\s+(call|tip|calls)", r"multibagger",
   r"(पक्की|पक्का)\s*टिप", r"इनसाइडर"]),
}
LINK_RE = re.compile(r"https?://[^\s]+|\b(?:bit\.ly|t\.ly|tinyurl\.com|rb\.gy|cutt\.ly)/\S+|\bwww\.[^\s]+", re.I)
NEG_RE = re.compile(r"\b(no|not|never|without|don't|dont|isn't|aren't|cannot)\b|नहीं|कभी|मत|(?<!\S)न(?!\S)", F)
LEVELS = [(6, "high_concern"), (3, "moderate_concern"), (1, "low_concern"), (0, "no_known_patterns")]
COMPILED = {k: [re.compile(p, F) for p in v[6]] for k, v in RULES.items()}

CATEGORY = {
 "high_concern": ("Several strong warning patterns", "कई मज़बूत चेतावनी संकेत",
   "Multiple well-known scam patterns appear together. Treat as high concern until verified through official sources.",
   "कई जाने-पहचाने ठगी संकेत एक साथ दिखे। आधिकारिक स्रोत से पुष्टि होने तक इसे अत्यधिक सावधानी से लें।"),
 "moderate_concern": ("Some warning patterns", "कुछ चेतावनी संकेत",
   "One serious or several weaker patterns appear. Do not act on this message until you verify the sender independently.",
   "एक गंभीर या कई कमज़ोर संकेत दिखे। प्रेषक की स्वतंत्र पुष्टि के बिना इस संदेश पर कार्रवाई न करें।"),
 "low_concern": ("Weak signals only", "केवल कमज़ोर संकेत",
   "Only minor signals were found. These also appear in genuine messages, so context matters.",
   "केवल हल्के संकेत मिले। ये असली संदेशों में भी होते हैं, इसलिए संदर्भ महत्वपूर्ण है।"),
 "no_known_patterns": ("No known patterns detected", "कोई ज्ञात संकेत नहीं मिला",
   "None of this tool's known patterns were found. This does NOT mean the message is safe or genuine.",
   "इस टूल के ज्ञात संकेतों में से कोई नहीं मिला। इसका मतलब यह नहीं कि संदेश सुरक्षित या असली है।"),
 "insufficient_text": ("Not enough text to analyse", "विश्लेषण के लिए पर्याप्त पाठ नहीं",
   "The text is too short for a meaningful analysis.", "पाठ इतना छोटा है कि सार्थक विश्लेषण संभव नहीं।"),
}
RECS = {
 "base": (["Do not reply, click links, scan QR codes or send money based on this message.",
           "Never share OTPs, passwords, PINs or card details with anyone.",
           "Verify the sender through an official website or phone number you find yourself, not one given in the message.",
           "Check whether any person or firm offering investment advice is registered, using official regulator resources (see Resources)."],
          ["इस संदेश के आधार पर जवाब न दें, लिंक न खोलें, QR स्कैन न करें और पैसे न भेजें।",
           "OTP, पासवर्ड, PIN या कार्ड विवरण किसी को न बताएं।",
           "प्रेषक की पुष्टि संदेश में दिए नंबर/लिंक से नहीं, बल्कि खुद खोजी गई आधिकारिक वेबसाइट या नंबर से करें।",
           "निवेश सलाह देने वाले व्यक्ति/कंपनी का पंजीकरण आधिकारिक नियामक संसाधनों से जाँचें (संसाधन पेज देखें)।"]),
 "serious": (["If you already paid or shared details, contact your bank immediately and use the official reporting options listed under Resources.",
              "Keep screenshots as records, and talk to a trusted family member before doing anything."],
             ["यदि आप पैसे भेज चुके हैं या जानकारी साझा कर चुके हैं, तुरंत अपने बैंक से संपर्क करें और संसाधन पेज पर दिए आधिकारिक रिपोर्टिंग विकल्प उपयोग करें।",
              "सबूत के रूप में स्क्रीनशॉट रखें और कुछ भी करने से पहले किसी भरोसेमंद परिवारजन से बात करें।"]),
}
UNCERTAINTY = ("This is keyword/pattern matching, not a verdict. It can miss new scams and can flag genuine messages. Confidence: low to moderate at best.",
               "यह कीवर्ड/पैटर्न मिलान है, कोई निर्णय नहीं। यह नई ठगियाँ चूक सकता है और असली संदेशों को भी चिह्नित कर सकता है। भरोसा: अधिकतम कम से मध्यम।")
DISCLAIMER = ("NiveshRakshak AI is an educational safety-assistance prototype. Automated results are not definitive fraud determinations, legal advice, or investment recommendations. Verify important information using official sources.",
              "निवेशरक्षक AI एक शैक्षिक सुरक्षा-सहायता प्रोटोटाइप है। स्वचालित परिणाम धोखाधड़ी का अंतिम निर्णय, कानूनी सलाह या निवेश सिफ़ारिश नहीं हैं। महत्वपूर्ण जानकारी आधिकारिक स्रोतों से सत्यापित करें।")


def detect_language(text):
    dev = sum(1 for c in text if "\u0900" <= c <= "\u097f")
    letters = sum(1 for c in text if c.isalpha()) or 1
    return "hi" if dev / letters > 0.3 else "en"


def _i(lang):
    return 1 if lang == "hi" else 0


def analyze_message(text, lang="en"):
    """Return structured analysis dict. Raises ValueError for non-string/too-long input."""
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if len(text) > MAX_TEXT_LEN:
        raise ValueError("text too long")
    lang = "hi" if lang == "hi" else "en"
    k = _i(lang)
    text = text.replace("\x00", "")
    detected_lang = detect_language(text)
    base = {"status": "ok", "language": lang, "detected_text_language": detected_lang,
            "disclaimer": DISCLAIMER[k], "uncertainty": UNCERTAINTY[k], "engine": "rules-v1"}
    if len(text.strip()) < MIN_TEXT_LEN:
        cat = "insufficient_text"
        return {**base, "result_category": cat, "result_label": CATEGORY[cat][k], "category_meaning": CATEGORY[cat][2 + k],
                "risk_score": 0, "detected_indicators": [], "evidence": [], "explanation": CATEGORY[cat][2 + k],
                "recommendations": []}
    indicators, evidence, score = [], [], 0
    for rid, rule in RULES.items():
        hits = []
        for rx in COMPILED[rid]:
            for m in rx.finditer(text):
                window = text[max(0, m.start() - 25): m.end() + 12]
                if rule[5] and NEG_RE.search(window):
                    continue
                hits.append((m.start(), m.end()))
        if hits:
            score += rule[0]
            indicators.append({"id": rid, "label": rule[1 + k], "explanation": rule[3 + k], "weight": rule[0]})
            for s, e in sorted(set(hits))[:3]:
                evidence.append({"indicator": rid, "quote": text[s:e], "start": s, "end": e})
    link_hits = []
    for m in LINK_RE.finditer(text):
        r = urlcheck.check_url(m.group(0).rstrip(".,;)"))
        if r.get("ok") and r["level"] in ("medium", "high"):
            link_hits.append((m, r))
    if link_hits:
        w = 3 if any(r['level'] == 'high' for _, r in link_hits) else 2
        score += w
        indicators.append({"id": "suspicious_link", "label": ("Link with suspicious address features" if k == 0 else "संदिग्ध विशेषताओं वाला लिंक"),
                           "explanation": ("The link's address shows suspicious features. Do not open it; use the URL analyzer for details." if k == 0 else
                                           "लिंक के पते में संदिग्ध विशेषताएँ हैं। इसे न खोलें; विवरण के लिए URL विश्लेषक देखें।"), "weight": w})
        for m, _ in link_hits[:3]:
            evidence.append({"indicator": "suspicious_link", "quote": m.group(0), "start": m.start(), "end": m.end()})
    cat = next(c for t, c in LEVELS if score >= t)
    recs = []
    if cat != "no_known_patterns":
        recs = RECS["base"][k] + (RECS["serious"][k] if cat in ("moderate_concern", "high_concern") else [])
    else:
        recs = RECS["base"][k][2:]
    expl = CATEGORY[cat][2 + k] if not indicators else " ".join(i["explanation"] for i in indicators)
    return {**base, "result_category": cat, "result_label": CATEGORY[cat][k], "category_meaning": CATEGORY[cat][2 + k],
            "risk_score": score, "detected_indicators": indicators, "evidence": evidence,
            "explanation": expl, "recommendations": recs}


def analyze_url(raw, lang="en"):
    lang = "hi" if lang == "hi" else "en"
    k = _i(lang)
    r = urlcheck.check_url(raw)
    if not r["ok"]:
        msgs = {"empty": ("Please enter a link.", "कृपया एक लिंक दर्ज करें।"),
                "scheme": ("Only http/https links can be examined.", "केवल http/https लिंक की जाँच की जा सकती है।"),
                "invalid": ("This does not look like a valid link.", "यह मान्य लिंक नहीं लगता।")}
        raise ValueError(msgs.get(r["error"], msgs["invalid"])[k])
    inds, ev = [], []
    for iid, quote in r["indicators"]:
        t = urlcheck.T[iid]
        inds.append({"id": iid, "label": t[1 + k], "explanation": t[3 + k], "weight": t[0]})
        ev.append({"indicator": iid, "quote": quote})
    lvl = {"high": "high_concern", "medium": "moderate_concern", "low": "low_concern", "none": "no_known_patterns"}[r["level"]]
    note = ("Basic offline heuristics only. The link was NOT opened and NOT checked against any threat-intelligence database."
            if k == 0 else "केवल बुनियादी ऑफ़लाइन जाँच। लिंक खोला नहीं गया और किसी थ्रेट-इंटेलिजेंस डेटाबेस से मिलाया नहीं गया।")
    return {"status": "ok", "language": lang, "result_category": lvl, "result_label": CATEGORY[lvl][k],
            "category_meaning": CATEGORY[lvl][2 + k], "risk_score": r["score"], "host": r["host"],
            "detected_indicators": inds, "evidence": ev,
            "explanation": " ".join(i["explanation"] for i in inds) or CATEGORY[lvl][2 + k],
            "recommendations": RECS["base"][k][:1] + RECS["base"][k][2:3] if inds else RECS["base"][k][2:3],
            "threat_intelligence": {"checked": False, "note": note},
            "uncertainty": UNCERTAINTY[k], "disclaimer": DISCLAIMER[k], "engine": "url-heuristics-v1"}
