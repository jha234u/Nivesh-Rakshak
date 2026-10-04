"""Rule-based safety assistant (offline). No LLM is called; see docs for the planned LLM hook."""
import re
F = re.I | re.U
MAX_Q = 1000
REFUSE_RX = [re.compile(p, F) for p in [
    r"\b(which|what)\s+(stocks?|shares?|funds?|crypto\w*|coins?)\b.*\b(buy|sell|invest|best)", r"\bshould\s+i\s+(buy|sell|hold|invest)\b",
    r"\b(price|target)\s+(prediction|target|forecast)", r"\bwill\b.*\b(go\s+up|rise|double|crash)\b", r"\bbest\s+(stock|share|broker|scheme)\b",
    r"कौन\s*सा\s*(शेयर|स्टॉक|फंड)", r"(खरीदूँ|खरीदूं|बेचूँ|बेचूं|खरीदें या बेचें)", r"कितना\s*रिटर्न\s*मिलेगा"]]
SECRET_RX = re.compile(r"\b\d{6}\b|my\s+(otp|password|pin)\s+is|मेरा\s*(ओटीपी|पासवर्ड|पिन)", F)
T = [  # (keywords, en, hi)
 (r"already\s+(paid|sent|lost)|lost\s+money|cheated|defrauded|पैसे\s*(भेज\s*दिए|गँवा|खो)|ठगी\s*हो",
  "Act quickly: (1) call your bank/UPI app support through its official number and ask to block further transactions, (2) report through the official channels on the Resources page, (3) keep screenshots and transaction IDs, (4) stop all contact with the sender. Recovery is not guaranteed, but fast reporting helps.",
  "तुरंत कदम उठाएँ: (1) अपने बैंक/UPI ऐप के आधिकारिक नंबर पर कॉल कर आगे के लेन-देन रोकने को कहें, (2) संसाधन पेज पर दिए आधिकारिक माध्यम से रिपोर्ट करें, (3) स्क्रीनशॉट और ट्रांज़ैक्शन ID सुरक्षित रखें, (4) ठग से संपर्क बंद करें। पैसे वापस मिलने की गारंटी नहीं, पर जल्दी रिपोर्ट करना मदद करता है।"),
 (r"\botp\b|password|\bpin\b|cvv|ओटीपी|पासवर्ड|पिन",
  "Never share an OTP, password, PIN or CVV with anyone, including people claiming to be from your bank, a broker or the government. Genuine organisations do not ask for them. NiveshRakshak AI will never ask for them either.",
  "OTP, पासवर्ड, PIN या CVV किसी को न बताएं, चाहे वह बैंक, ब्रोकर या सरकार का बनकर बात करे। असली संस्थाएँ इन्हें नहीं माँगतीं। निवेशरक्षक AI भी कभी नहीं माँगेगा।"),
 (r"guarantee|assured|double|risk[- ]?free|high\s+return|गारंटी|दोगुना|बिना\s*जोखिम|ऊँचा\s*रिटर्न",
  "No genuine investment can guarantee returns. Higher promised returns usually mean higher risk or a scam. Be wary of 'risk-free', 'assured' or 'double your money' claims.",
  "कोई असली निवेश रिटर्न की गारंटी नहीं दे सकता। ज़्यादा वादा किया गया रिटर्न अक्सर ज़्यादा जोखिम या ठगी का संकेत है। 'बिना जोखिम', 'पक्का' या 'पैसा दोगुना' के दावों से सावधान रहें।"),
 (r"whatsapp|telegram|group|tip|व्हाट्सएप|टेलीग्राम|ग्रुप|टिप",
  "Unsolicited WhatsApp/Telegram 'tips' groups are a common scam channel. Do not follow tips from strangers, and never transfer money to a personal account or UPI ID to 'join' or 'activate' anything.",
  "अनजान WhatsApp/Telegram 'टिप्स' ग्रुप ठगी का आम ज़रिया हैं। अजनबियों की टिप न मानें और ग्रुप 'जुड़ने' या 'सक्रिय' करने के लिए किसी निजी खाते/UPI ID में पैसे न भेजें।"),
 (r"phish|link|fake\s+(site|website|app)|लिंक|फ़िशिंग|फर्जी|नकली",
  "Do not tap links in unexpected messages. Type the official website address yourself, check for look-alike spellings, and install apps only from official app stores. Use the URL analyzer here to examine a link safely (it never opens it).",
  "अनचाहे संदेशों के लिंक पर टैप न करें। आधिकारिक वेबसाइट का पता खुद टाइप करें, मिलते-जुलते वर्तनी पर ध्यान दें और ऐप केवल आधिकारिक ऐप स्टोर से लें। लिंक को सुरक्षित रूप से जाँचने के लिए यहाँ URL विश्लेषक उपयोग करें (यह लिंक नहीं खोलता)।"),
 (r"sebi|registered|register|license|पंजीकृत|रजिस्टर",
  "You can check whether an adviser, broker or intermediary is registered on the regulator's official website (see the Resources page). A claim of registration inside a message is not proof; always check it yourself.",
  "आप नियामक की आधिकारिक वेबसाइट पर जाँच सकते हैं कि सलाहकार/ब्रोकर पंजीकृत है या नहीं (संसाधन पेज देखें)। संदेश में पंजीकरण का दावा प्रमाण नहीं है; खुद जाँचें।"),
 (r"report|complain|helpline|1930|शिकायत|रिपोर्ट|हेल्पलाइन",
  "The Resources page lists official reporting options (cybercrime portal, helpline, regulator complaint systems). Please verify each listing before use.",
  "संसाधन पेज पर आधिकारिक रिपोर्टिंग विकल्प (साइबर अपराध पोर्टल, हेल्पलाइन, नियामक शिकायत प्रणाली) दिए हैं। उपयोग से पहले हर प्रविष्टि सत्यापित करें।"),
 (r"scam|fraud|suspicious|safe|ठगी|धोखा|संदिग्ध|सुरक्षित",
  "Common warning signs: guaranteed returns, pressure to act fast, requests for OTP/passwords, payment to personal accounts, secret tips, and claims of approval you cannot verify. Paste the message into the analyzer to see which signs appear.",
  "आम चेतावनी संकेत: गारंटीशुदा रिटर्न, जल्दी करने का दबाव, OTP/पासवर्ड की माँग, निजी खाते में भुगतान, गुप्त टिप और ऐसी मंज़ूरी के दावे जिन्हें जाँचा न जा सके। कौन-से संकेत हैं यह देखने के लिए संदेश विश्लेषक में चिपकाएँ।"),
]
T = [(re.compile(p, F), e, h) for p, e, h in T]
REFUSAL = ("I can't recommend stocks or products, or predict prices or returns. I can help you spot scams, understand risks and find official resources. Please consult a SEBI-registered adviser for personal investment decisions.",
           "मैं शेयर/उत्पाद नहीं सुझा सकता, न ही कीमत या रिटर्न का अनुमान दे सकता हूँ। मैं ठगी पहचानने, जोखिम समझने और आधिकारिक संसाधन खोजने में मदद कर सकता हूँ। निजी निवेश निर्णय के लिए सेबी-पंजीकृत सलाहकार से परामर्श लें।")
SECRET = ("Please do not share OTPs, passwords or PINs here or with anyone. I did not store this. Delete it from the chat box.",
          "कृपया OTP, पासवर्ड या PIN यहाँ या किसी को न बताएं। मैंने इसे सहेजा नहीं। इसे चैट बॉक्स से हटा दें।")
DEFAULT = ("I can help with spotting suspicious messages, phishing, protecting your information and finding official reporting resources. Try asking: 'How do I know if an investment offer is a scam?'",
           "मैं संदिग्ध संदेश पहचानने, फ़िशिंग, अपनी जानकारी सुरक्षित रखने और आधिकारिक रिपोर्टिंग संसाधन खोजने में मदद कर सकता हूँ। पूछें: 'निवेश का ऑफर ठगी है या नहीं कैसे पता करें?'")
NOTE = ("General safety information only, not investment or legal advice.", "केवल सामान्य सुरक्षा जानकारी; निवेश या कानूनी सलाह नहीं।")


def chat(message, lang="en"):
    if not isinstance(message, str) or not message.strip():
        raise ValueError("message required")
    if len(message) > MAX_Q:
        raise ValueError("message too long")
    k = 1 if lang == "hi" else 0
    lang = "hi" if k else "en"
    out = {"status": "ok", "language": lang, "source": "rules", "disclaimer": NOTE[k]}
    if SECRET_RX.search(message):
        return {**out, "kind": "secret_warning", "answer": SECRET[k]}
    if any(r.search(message) for r in REFUSE_RX):
        return {**out, "kind": "refusal", "answer": REFUSAL[k]}
    for rx, en, hi in T:
        if rx.search(message):
            return {**out, "kind": "answer", "answer": (en, hi)[k]}
    return {**out, "kind": "default", "answer": DEFAULT[k]}
