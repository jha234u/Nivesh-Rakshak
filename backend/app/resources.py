"""Official resources. IMPORTANT: written from the author's knowledge; the build environment had no
internet access, so NONE of these were live-verified. Every entry is flagged for manual verification."""
RESOURCES = [
 {"id": "ncrp", "name": {"en": "National Cyber Crime Reporting Portal", "hi": "राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल"},
  "url": "https://cybercrime.gov.in", "use": {"en": "Report online financial fraud and other cybercrime.", "hi": "ऑनलाइन वित्तीय धोखाधड़ी और अन्य साइबर अपराध की रिपोर्ट करें।"}},
 {"id": "helpline1930", "name": {"en": "Cyber crime helpline 1930", "hi": "साइबर अपराध हेल्पलाइन 1930"},
  "url": None, "phone": "1930", "use": {"en": "Phone helpline for reporting financial cyber fraud quickly.", "hi": "वित्तीय साइबर धोखाधड़ी की तुरंत रिपोर्ट के लिए फ़ोन हेल्पलाइन।"}},
 {"id": "scores", "name": {"en": "SEBI SCORES (investor complaints)", "hi": "सेबी स्कोर्स (निवेशक शिकायत)"},
  "url": "https://scores.sebi.gov.in", "use": {"en": "Lodge complaints against SEBI-regulated entities.", "hi": "सेबी-विनियमित संस्थाओं के विरुद्ध शिकायत दर्ज करें।"}},
 {"id": "sebi", "name": {"en": "SEBI (securities regulator) website", "hi": "सेबी (प्रतिभूति नियामक) वेबसाइट"},
  "url": "https://www.sebi.gov.in", "use": {"en": "Look up registered intermediaries and read investor alerts.", "hi": "पंजीकृत मध्यस्थों की जाँच करें और निवेशक चेतावनियाँ पढ़ें।"}},
 {"id": "sebi_investor", "name": {"en": "SEBI investor education site", "hi": "सेबी निवेशक शिक्षा साइट"},
  "url": "https://investor.sebi.gov.in", "use": {"en": "Investor awareness material and guidance.", "hi": "निवेशक जागरूकता सामग्री और मार्गदर्शन।"}},
 {"id": "sachet", "name": {"en": "RBI Sachet", "hi": "आरबीआई सचेत"},
  "url": "https://sachet.rbi.org.in", "use": {"en": "Check entities accepting deposits and report unauthorised ones.", "hi": "जमा स्वीकारने वाली संस्थाओं की जाँच करें और अनधिकृत की शिकायत करें।"}},
 {"id": "sanchar", "name": {"en": "Sanchar Saathi (DoT)", "hi": "संचार साथी (दूरसंचार विभाग)"},
  "url": "https://sancharsaathi.gov.in", "use": {"en": "Report suspected fraud calls/messages and check mobile connections in your name.", "hi": "संदिग्ध ठगी कॉल/संदेश की रिपोर्ट करें और अपने नाम के मोबाइल कनेक्शन जाँचें।"}},
]
for r in RESOURCES:
    r["verification"] = "needs_manual_verification"
    r["verified_on"] = None
