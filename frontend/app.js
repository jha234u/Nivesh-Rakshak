"use strict";
/* NiveshRakshak AI frontend. No frameworks, no inline scripts, no innerHTML with user data (XSS-safe by construction). */
const S = {
en: {
 nav:{home:"Home",analyze:"Check a message",assistant:"Ask for help",learn:"Learn",resources:"Official help",privacy:"Privacy & About"},
 banner:"Educational prototype. Results are not definitive fraud determinations, legal advice or investment recommendations. Verify with official sources.",
 h1:"Your smart shield against digital financial scams",
 sub:"Paste a suspicious message, link or screenshot. We show which warning signs appear, quote the exact words, and explain what to do next, in simple English or Hindi.",
 cta:"Analyze a message", cta2:"Try the learning quiz",
 problem:"The problem", problemT:"Fake investment offers, phishing links and 'guaranteed return' tips reach millions through WhatsApp and social media. Many first-time investors, especially in smaller cities and regional-language communities, have no easy way to judge them.",
 solution:"Our approach", solutionT:"A transparent checker that shows its evidence, says when it is unsure, never gives stock tips, and works in Hindi and English.",
 how:"How it works", steps:["Paste a message, link or upload a screenshot","See warning signs with exact quotes","Follow plain-language safety steps"],
 feats:[["Message checker","Finds warning patterns and quotes the evidence."],["Link checker","Examines a link's address without ever opening it."],["Screenshot reader","Reads text from a screenshot, then checks it."],["Safety assistant","Answers scam-safety questions. Never gives stock tips."],["Learning zone","5 realistic practice scenarios with a score."],["Official help","Reporting and verification resources."]],
 tMsg:"Message",tUrl:"Link",tImg:"Screenshot", msgPh:"Paste the suspicious message here…", urlPh:"Paste a link (it will NOT be opened)",
 check:"Check", checking:"Checking…", sample:"Use a sample message", sampleText:"Congratulations! Guaranteed 30% monthly returns, risk-free. SEBI registered. Hurry, only 20 seats left! Join our VIP WhatsApp group and pay a registration fee of Rs 2000 to UPI id raj@upi. Share your OTP to activate.",
 dontShare:"Do not paste OTPs, passwords or card numbers here.", imgHelp:"Upload a PNG, JPEG or WebP screenshot (max 5 MB). It is read in memory and not stored.",
 extracted:"Text read from the screenshot (please check it)", result:"Result", meaning:"What this category means", indicators:"Warning signs found", evidence:"Exact words from your message", explain:"Why this matters", next:"What you can do now",
 unc:"How sure is this?", none:"No warning patterns were found. That is not proof that it is safe.", threat:"Link status",
 err:"Something went wrong. Please try again.", net:"Could not reach the server. Is it running?",
 asstH:"Safety assistant", asstIntro:"Ask about scams, phishing, protecting your information or where to report. I do not give stock tips or predict returns.", asstPh:"Type your question…", send:"Send",
 asstChips:["How do I know if an investment offer is a scam?","What should I do if I already paid?","Which stock should I buy?"],
 learnH:"Learning zone", q:"What is the biggest warning sign here?", next2:"Next", finish:"See my score", score:"Your score", of:"of", again:"Try again", tip:"Safety tip", right:"Correct.", wrong:"Not quite.",
 done:["Great awareness!","Good start. Review the tips.","Keep practising. These patterns are learnable."],
 resH:"Official help and reporting", resNote:"These entries are not live-verified. Confirm each link or number on the official source before relying on it.", open:"Open official site", vstat:"Needs manual verification", call:"Phone",
 privH:"Privacy & About", priv:["We do not ask for or store OTPs, passwords or bank details.","Messages and screenshots are processed in memory and not saved. No accounts, no tracking.","Only your language choice is kept in your browser.","No external AI service is called in this version; analysis is rule-based and runs on this server."],
 aboutH:"About this prototype", about:"NiveshRakshak AI was built for the SANGYAN hackathon (Investor Protection and Public-Good Technology). It looks for known warning patterns; it cannot verify who sent a message or whether a firm is genuine.",
 disc:"NiveshRakshak AI is an educational safety-assistance prototype. Automated results are not definitive fraud determinations, legal advice, or investment recommendations. Verify important information using official sources.",
},
hi: {
 nav:{home:"होम",analyze:"संदेश जाँचें",assistant:"मदद पूछें",learn:"सीखें",resources:"आधिकारिक मदद",privacy:"गोपनीयता और परिचय"},
 banner:"शैक्षिक प्रोटोटाइप। परिणाम धोखाधड़ी का अंतिम निर्णय, कानूनी सलाह या निवेश सिफ़ारिश नहीं हैं। आधिकारिक स्रोत से सत्यापित करें।",
 h1:"डिजिटल वित्तीय ठगी के विरुद्ध आपकी स्मार्ट ढाल",
 sub:"कोई संदिग्ध संदेश, लिंक या स्क्रीनशॉट डालें। हम बताते हैं कौन-से चेतावनी संकेत हैं, उनके सटीक शब्द दिखाते हैं और आगे क्या करें यह सरल हिंदी/अंग्रेज़ी में समझाते हैं।",
 cta:"संदेश जाँचें", cta2:"सीखने की क्विज़ आज़माएँ",
 problem:"समस्या", problemT:"नकली निवेश ऑफ़र, फ़िशिंग लिंक और 'गारंटीशुदा रिटर्न' की टिप WhatsApp और सोशल मीडिया से करोड़ों लोगों तक पहुँचती हैं। छोटे शहरों और क्षेत्रीय भाषा के कई नए निवेशकों के पास इन्हें परखने का आसान तरीका नहीं है।",
 solution:"हमारा तरीका", solutionT:"एक पारदर्शी जाँचकर्ता जो सबूत दिखाता है, अनिश्चित होने पर बताता है, कभी शेयर टिप नहीं देता और हिंदी-अंग्रेज़ी दोनों में काम करता है।",
 how:"यह कैसे काम करता है", steps:["संदेश या लिंक डालें, या स्क्रीनशॉट अपलोड करें","सटीक उद्धरणों के साथ चेतावनी संकेत देखें","सरल भाषा में सुरक्षा कदम अपनाएँ"],
 feats:[["संदेश जाँच","चेतावनी पैटर्न खोजता है और सबूत उद्धृत करता है।"],["लिंक जाँच","लिंक को खोले बिना उसके पते की जाँच करता है।"],["स्क्रीनशॉट रीडर","स्क्रीनशॉट से पाठ पढ़कर जाँचता है।"],["सुरक्षा सहायक","ठगी-सुरक्षा के सवालों के जवाब। शेयर टिप कभी नहीं।"],["सीखने का क्षेत्र","स्कोर के साथ 5 यथार्थ अभ्यास परिदृश्य।"],["आधिकारिक मदद","रिपोर्टिंग और सत्यापन संसाधन।"]],
 tMsg:"संदेश",tUrl:"लिंक",tImg:"स्क्रीनशॉट", msgPh:"संदिग्ध संदेश यहाँ चिपकाएँ…", urlPh:"लिंक चिपकाएँ (इसे खोला नहीं जाएगा)",
 check:"जाँचें", checking:"जाँच जारी…", sample:"नमूना संदेश उपयोग करें", sampleText:"बधाई हो! 30% मासिक गारंटीशुदा रिटर्न, बिना जोखिम। सेबी पंजीकृत। जल्दी करें, केवल 20 सीट बाकी! हमारे VIP व्हाट्सएप ग्रुप से जुड़ें और यूपीआई id raj@upi पर 2000 रुपये जमा करें। सक्रिय करने के लिए अपना ओटीपी बताएं।",
 dontShare:"यहाँ OTP, पासवर्ड या कार्ड नंबर न डालें।", imgHelp:"PNG, JPEG या WebP स्क्रीनशॉट अपलोड करें (अधिकतम 5 MB)। इसे मेमोरी में पढ़ा जाता है, सहेजा नहीं जाता।",
 extracted:"स्क्रीनशॉट से पढ़ा गया पाठ (कृपया जाँच लें)", result:"परिणाम", meaning:"इस श्रेणी का अर्थ", indicators:"मिले चेतावनी संकेत", evidence:"आपके संदेश के सटीक शब्द", explain:"यह क्यों मायने रखता है", next:"अब आप क्या कर सकते हैं",
 unc:"यह कितना पक्का है?", none:"कोई चेतावनी पैटर्न नहीं मिला। यह सुरक्षित होने का प्रमाण नहीं है।", threat:"लिंक की स्थिति",
 err:"कुछ गलत हुआ। कृपया फिर कोशिश करें।", net:"सर्वर तक नहीं पहुँच सके। क्या वह चल रहा है?",
 asstH:"सुरक्षा सहायक", asstIntro:"ठगी, फ़िशिंग, अपनी जानकारी सुरक्षित रखने या शिकायत कहाँ करें, इस बारे में पूछें। मैं शेयर टिप नहीं देता और रिटर्न का अनुमान नहीं लगाता।", asstPh:"अपना सवाल लिखें…", send:"भेजें",
 asstChips:["निवेश का ऑफर ठगी है या नहीं कैसे पता करें?","अगर मैं पैसे भेज चुका हूँ तो क्या करूँ?","कौन सा शेयर खरीदूँ?"],
 learnH:"सीखने का क्षेत्र", q:"यहाँ सबसे बड़ा चेतावनी संकेत क्या है?", next2:"आगे", finish:"मेरा स्कोर देखें", score:"आपका स्कोर", of:"में से", again:"फिर कोशिश करें", tip:"सुरक्षा सुझाव", right:"सही।", wrong:"बिल्कुल सही नहीं।",
 done:["शानदार जागरूकता!","अच्छी शुरुआत। सुझाव दोबारा पढ़ें।","अभ्यास जारी रखें। ये संकेत सीखे जा सकते हैं।"],
 resH:"आधिकारिक मदद और रिपोर्टिंग", resNote:"ये प्रविष्टियाँ लाइव-सत्यापित नहीं हैं। भरोसा करने से पहले हर लिंक/नंबर आधिकारिक स्रोत पर जाँचें।", open:"आधिकारिक साइट खोलें", vstat:"मैन्युअल सत्यापन आवश्यक", call:"फ़ोन",
 privH:"गोपनीयता और परिचय", priv:["हम OTP, पासवर्ड या बैंक विवरण न माँगते हैं, न सहेजते हैं।","संदेश और स्क्रीनशॉट मेमोरी में प्रोसेस होते हैं और सहेजे नहीं जाते। कोई खाता या ट्रैकिंग नहीं।","केवल आपकी भाषा पसंद आपके ब्राउज़र में रखी जाती है।","इस संस्करण में कोई बाहरी AI सेवा नहीं बुलाई जाती; विश्लेषण नियम-आधारित है और इसी सर्वर पर चलता है।"],
 aboutH:"इस प्रोटोटाइप के बारे में", about:"निवेशरक्षक AI सांग्यान हैकाथॉन (निवेशक संरक्षण और जनहित प्रौद्योगिकी) के लिए बनाया गया। यह ज्ञात चेतावनी पैटर्न खोजता है; यह सत्यापित नहीं कर सकता कि संदेश किसने भेजा या कंपनी असली है या नहीं।",
 disc:"निवेशरक्षक AI एक शैक्षिक सुरक्षा-सहायता प्रोटोटाइप है। स्वचालित परिणाम धोखाधड़ी का अंतिम निर्णय, कानूनी सलाह या निवेश सिफ़ारिश नहीं हैं। महत्वपूर्ण जानकारी आधिकारिक स्रोतों से सत्यापित करें।",
}};
const QUIZ = [
 {m:{en:"🔥 Invest ₹10,000 today and get ₹30,000 in 15 days! 100% guaranteed. Only 20 seats left!",hi:"🔥 आज ₹10,000 लगाएँ और 15 दिन में ₹30,000 पाएँ! 100% गारंटी। केवल 20 सीट बाकी!"},
  o:{en:["Guaranteed returns and pressure to hurry","It uses emojis","It mentions rupees"],hi:["गारंटीशुदा रिटर्न और जल्दी करने का दबाव","इसमें इमोजी हैं","इसमें रुपयों का ज़िक्र है"]},c:0,
  w:{en:"No honest investment can guarantee a 200% gain, and 'only 20 seats' is made-up scarcity to stop you from checking.",hi:"कोई ईमानदार निवेश 200% लाभ की गारंटी नहीं दे सकता, और 'केवल 20 सीट' बनावटी कमी है जो आपको जाँचने से रोकती है।"},
  t:{en:"Ask: who is paying me this, and where can I verify it independently?",hi:"पूछें: यह रिटर्न कौन देगा, और मैं इसे स्वतंत्र रूप से कहाँ जाँच सकता हूँ?"}},
 {m:{en:"Dear customer, your demat account will be blocked today. Update KYC at http://kyc-update-demat.xyz/login and enter the OTP you receive.",hi:"प्रिय ग्राहक, आपका डीमैट खाता आज ब्लॉक हो जाएगा। http://kyc-update-demat.xyz/login पर KYC अपडेट करें और मिला OTP डालें।"},
  o:{en:["It addresses you as 'customer'","Threat + unknown link + request for OTP","It mentions KYC"],hi:["यह आपको 'ग्राहक' कहता है","धमकी + अनजान लिंक + OTP की माँग","इसमें KYC का ज़िक्र है"]},c:1,
  w:{en:"This is a typical phishing pattern: a threat creates fear, an unfamiliar address collects your details, and the OTP would let someone take over your account.",hi:"यह फ़िशिंग का आम तरीका है: धमकी डर पैदा करती है, अनजान पता आपकी जानकारी लेता है, और OTP से कोई आपके खाते पर कब्ज़ा कर सकता है।"},
  t:{en:"Never tap such links. Open your broker's app or type its official address yourself.",hi:"ऐसे लिंक पर कभी टैप न करें। अपने ब्रोकर का ऐप खोलें या उसका आधिकारिक पता खुद टाइप करें।"}},
 {m:{en:"I am from the SEBI cyber cell. Your account is linked to illegal activity. Pay ₹15,000 as a security deposit to UPI id officer@upi to avoid arrest.",hi:"मैं सेबी साइबर सेल से हूँ। आपका खाता अवैध गतिविधि से जुड़ा है। गिरफ़्तारी से बचने के लिए UPI id officer@upi पर ₹15,000 सुरक्षा जमा करें।"},
  o:{en:["A regulator demanding money to a personal UPI ID","The officer gave a UPI id","It mentions arrest"],hi:["नियामक का निजी UPI ID पर पैसे माँगना","अधिकारी ने UPI id दी","इसमें गिरफ़्तारी का ज़िक्र है"]},c:0,
  w:{en:"Genuine authorities do not collect 'deposits' by UPI to avoid arrest. Impersonating officials and creating fear is a common scam script.",hi:"असली अधिकारी गिरफ़्तारी से बचाने के नाम पर UPI से 'जमा' नहीं माँगते। अधिकारी बनकर डराना ठगी का आम तरीका है।"},
  t:{en:"Hang up, do not pay, and report it through the official channels on the Resources page.",hi:"कॉल काट दें, भुगतान न करें और संसाधन पेज के आधिकारिक माध्यम से रिपोर्ट करें।"}},
 {m:{en:"Our VIP group's operator call gives sure-shot 5x in 3 days. Pay a ₹2,000 joining fee now to get in.",hi:"हमारे VIP ग्रुप की ऑपरेटर कॉल 3 दिन में पक्का 5 गुना देती है। अभी ₹2,000 जॉइनिंग फ़ीस भरें।"},
  o:{en:["The group has a name","'Sure-shot' tip plus a fee to join","The number 5x"],hi:["ग्रुप का एक नाम है","'पक्की' टिप और जुड़ने की फ़ीस","5 गुना की संख्या"]},c:1,
  w:{en:"Nobody can know a sure outcome in markets. A paid 'tips' group is a common way to collect fees or to push you into a pump-and-dump.",hi:"बाज़ार में किसी को पक्के नतीजे का पता नहीं होता। पैसे वाला 'टिप्स' ग्रुप फ़ीस वसूलने या शेयर-उछाल ठगी में फँसाने का आम तरीका है।"},
  t:{en:"Do not follow tips from strangers, and do not pay to 'join' anything.",hi:"अजनबियों की टिप न मानें और कुछ भी 'जुड़ने' के लिए पैसे न दें।"}},
 {m:{en:"Our app is SEBI approved. Earn ₹5,000 daily with no risk. Download now from this link.",hi:"हमारा ऐप सेबी से मान्य है। बिना जोखिम रोज़ ₹5,000 कमाएँ। इस लिंक से अभी डाउनलोड करें।"},
  o:{en:["An approval claim you cannot verify, plus 'no risk' daily income","It says 'app'","It says 'download'"],hi:["ऐसा मंज़ूरी का दावा जो जाँचा नहीं जा सकता, और 'बिना जोखिम' रोज़ की कमाई","इसमें 'ऐप' लिखा है","इसमें 'डाउनलोड' लिखा है"]},c:0,
  w:{en:"Anyone can type 'approved'. Check the regulator's own website yourself. 'No risk' daily income is not something real investments offer.",hi:"'मान्य' कोई भी लिख सकता है। नियामक की अपनी वेबसाइट पर खुद जाँचें। 'बिना जोखिम' रोज़ की कमाई असली निवेश में नहीं मिलती।"},
  t:{en:"Install apps only from official app stores, after checking the company on the regulator's site.",hi:"ऐप केवल आधिकारिक ऐप स्टोर से लें, और पहले नियामक की साइट पर कंपनी की जाँच कर लें।"}}];
const st = {lang:"en", page:"home", tab:"msg", last:null, quiz:{i:0,score:0,answered:false,done:false}, chat:[]};
try { const l = localStorage.getItem("nr_lang"); if (l === "hi" || l === "en") st.lang = l; } catch (e) {}
const t = () => S[st.lang];
function h(tag, props, ...kids) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (k === "class") e.className = v; else if (k.startsWith("on")) e.addEventListener(k.slice(2), v);
    else if (v !== false && v != null) e.setAttribute(k, v);
  }
  for (const c of kids.flat()) if (c != null && c !== false) e.append(c.nodeType ? c : document.createTextNode(String(c)));
  return e;
}
async function api(path, opts) {
  const base = window.NR_API_BASE || "";
  const r = await fetch(base + path, opts);
  let j = {}; try { j = await r.json(); } catch (e) {}
  if (!r.ok || j.status === "error") throw new Error(j.message || t().err);
  return j;
}
const post = (path, obj) => api(path, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({...obj, language: st.lang})});

function go(p) { st.page = p; if (location.hash !== "#" + p) location.hash = p; render(); document.getElementById("view").focus(); window.scrollTo(0, 0); }
function renderShell() {
  document.documentElement.lang = st.lang;
  const nav = document.getElementById("nav"); nav.replaceChildren();
  for (const k of Object.keys(t().nav)) nav.append(h("a", {href: "#" + k, class: st.page === k ? "on" : "", "data-nav": k, onclick: ev => { ev.preventDefault(); go(k); }}, t().nav[k]));
  document.getElementById("banner").textContent = t().banner;
  document.getElementById("foot").textContent = t().disc;
  document.getElementById("l-en").className = st.lang === "en" ? "on" : "";
  document.getElementById("l-hi").className = st.lang === "hi" ? "on" : "";
}
function render() {
  renderShell();
  const v = document.getElementById("view"); v.replaceChildren();
  ({home: pHome, analyze: pAnalyze, assistant: pAssistant, learn: pLearn, resources: pResources, privacy: pPrivacy}[st.page] || pHome)(v);
}
function setLang(l) {
  st.lang = l; try { localStorage.setItem("nr_lang", l); } catch (e) {}
  render();
  if (st.page === "analyze" && st.last) rerun();
}

function pHome(v) {
  v.append(h("section", {class: "hero"}, h("h1", {}, t().h1), h("p", {}, t().sub),
    h("div", {class: "row"}, h("button", {class: "btn", type: "button", onclick: () => go("analyze")}, t().cta), h("button", {class: "btn sec", type: "button", onclick: () => go("learn")}, t().cta2))));
  v.append(h("div", {class: "grid"}, h("div", {class: "card"}, h("h2", {}, t().problem), h("p", {}, t().problemT)), h("div", {class: "card"}, h("h2", {}, t().solution), h("p", {}, t().solutionT))));
  v.append(h("h2", {}, t().how), h("div", {class: "grid"}, t().steps.map((s, i) => h("div", {class: "card"}, h("strong", {}, (i + 1) + ". "), s))));
  v.append(h("div", {class: "grid"}, t().feats.map(f => h("div", {class: "card"}, h("strong", {}, f[0]), h("p", {class: "note"}, f[1])))));
  v.append(h("div", {class: "warn"}, "🔒 " + t().priv[0] + " " + t().priv[1]));
}

function resultCard(r, kind) {
  const c = h("div", {class: "card", role: "region", "aria-live": "polite"});
  c.append(h("h2", {}, t().result), h("span", {class: "badge b-" + r.result_category}, r.result_label), h("p", {}, h("strong", {}, t().meaning + ": "), r.category_meaning));
  if (r.detected_indicators.length) {
    c.append(h("h3", {}, t().indicators), h("ul", {}, r.detected_indicators.map(i => h("li", {}, h("strong", {}, i.label)))));
    c.append(h("h3", {}, t().evidence), r.evidence.map(e => h("blockquote", {}, e.quote)));
    c.append(h("h3", {}, t().explain), h("p", {}, r.explanation));
  } else c.append(h("p", {}, t().none));
  if (r.threat_intelligence) c.append(h("p", {class: "warn"}, h("strong", {}, t().threat + ": "), r.threat_intelligence.note));
  if (r.recommendations && r.recommendations.length) c.append(h("h3", {}, t().next), h("ul", {}, r.recommendations.map(x => h("li", {}, x))));
  c.append(h("h3", {}, t().unc), h("p", {class: "note"}, r.uncertainty), h("p", {class: "note"}, r.disclaimer));
  return c;
}
async function run(btn, out, fn) {
  const label = btn.textContent; btn.disabled = true; btn.textContent = t().checking; out.replaceChildren();
  try { const r = await fn(); out.replaceChildren(...r); }
  catch (e) { out.replaceChildren(h("div", {class: "err", role: "alert"}, e instanceof TypeError ? t().net : e.message)); }
  finally { btn.disabled = false; btn.textContent = label; }
}
let rerun = () => {};
function pAnalyze(v) {
  v.append(h("h1", {}, t().nav.analyze));
  const tabs = h("div", {class: "tabs", role: "tablist"}); const body = h("div"); const out = h("div", {id: "out"});
  const defs = [["msg", t().tMsg], ["url", t().tUrl], ["img", t().tImg]];
  for (const [k, lab] of defs) tabs.append(h("button", {type: "button", role: "tab", class: st.tab === k ? "on" : "", onclick: () => { st.tab = k; st.last = null; render(); }}, lab));
  v.append(tabs, h("p", {class: "note"}, "🔒 " + t().dontShare), body, out);
  if (st.tab === "msg") {
    const ta = h("textarea", {placeholder: t().msgPh, maxlength: 5000, "aria-label": t().tMsg});
    const b = h("button", {class: "btn", type: "button"}, t().check);
    const doIt = async () => { if (!ta.value.trim()) return; st.last = {k: "msg", v: ta.value};
      await run(b, out, async () => [resultCard(await post("/api/analyze/message", {text: ta.value}))]); };
    b.addEventListener("click", doIt); rerun = () => { ta.value = st.last.v; doIt(); };
    body.append(ta, h("div", {class: "row"}, b, h("button", {class: "btn sec", type: "button", onclick: () => { ta.value = t().sampleText; }}, t().sample)));
  } else if (st.tab === "url") {
    const inp = h("input", {type: "text", placeholder: t().urlPh, maxlength: 2048, "aria-label": t().tUrl});
    const b = h("button", {class: "btn", type: "button"}, t().check);
    const doIt = async () => { if (!inp.value.trim()) return; st.last = {k: "url", v: inp.value};
      await run(b, out, async () => [resultCard(await post("/api/analyze/url", {url: inp.value}))]); };
    b.addEventListener("click", doIt); rerun = () => { inp.value = st.last.v; doIt(); };
    body.append(h("div", {class: "row"}, inp, b), h("p", {class: "note"}, "e.g. http://sebi-gov-in-invest.xyz/login"));
  } else {
    const f = h("input", {type: "file", accept: "image/png,image/jpeg,image/webp", "aria-label": t().tImg});
    const b = h("button", {class: "btn", type: "button"}, t().check);
    const doIt = async () => { const file = f.files[0]; if (!file) return;
      await run(b, out, async () => {
        const r = await api("/api/analyze/image", {method: "POST", headers: {"Content-Type": file.type + "; lang=" + st.lang}, body: file});
        st.last = {k: "msg", v: r.extracted_text};
        return [h("div", {class: "card"}, h("h3", {}, t().extracted), h("blockquote", {}, r.extracted_text)), resultCard(r)]; }); };
    b.addEventListener("click", doIt); rerun = () => { if (st.last) { st.tab = "msg"; render(); document.querySelector("textarea").value = st.last.v; document.querySelector(".btn:not(.sec)").click(); } };
    body.append(h("p", {class: "note"}, t().imgHelp), f, h("div", {class: "row"}, b));
  }
}
function pAssistant(v) {
  v.append(h("h1", {}, t().asstH), h("p", {}, t().asstIntro), h("p", {class: "note"}, "🔒 " + t().dontShare));
  const log = h("div", {class: "chat", "aria-live": "polite"}); const inp = h("input", {type: "text", placeholder: t().asstPh, maxlength: 1000, "aria-label": t().asstPh});
  const draw = () => { log.replaceChildren(...st.chat.map(m => h("div", {class: "msg " + m.r}, m.x))); log.scrollTop = log.scrollHeight; };
  const send = async txt => { txt = (txt || inp.value).trim(); if (!txt) return; inp.value = ""; st.chat.push({r: "u", x: txt}); draw();
    try { const r = await post("/api/assistant/chat", {message: txt}); st.chat.push({r: "a", x: r.answer + "\n\n" + r.disclaimer}); }
    catch (e) { st.chat.push({r: "a", x: e instanceof TypeError ? t().net : e.message}); } draw(); };
  inp.addEventListener("keydown", e => { if (e.key === "Enter") send(); });
  v.append(h("div", {class: "card"}, log, h("div", {class: "row"}, inp, h("button", {class: "btn", type: "button", onclick: () => send()}, t().send))),
    h("div", {class: "row"}, t().asstChips.map(c => h("button", {class: "btn sec", type: "button", onclick: () => send(c)}, c))));
  draw();
}
function pLearn(v) {
  const q = st.quiz; v.append(h("h1", {}, t().learnH));
  if (q.done) {
    const lvl = q.score >= 4 ? 0 : q.score >= 2 ? 1 : 2;
    v.append(h("div", {class: "card"}, h("h2", {}, t().score + ": " + q.score + " " + t().of + " " + QUIZ.length), h("p", {}, t().done[lvl]),
      h("button", {class: "btn", type: "button", onclick: () => { st.quiz = {i: 0, score: 0, answered: false, done: false}; render(); }}, t().again),
      h("button", {class: "btn sec", type: "button", onclick: () => go("analyze")}, t().cta))); return;
  }
  const s = QUIZ[q.i]; const L = st.lang;
  const card = h("div", {class: "card"}, h("small", {}, (q.i + 1) + " / " + QUIZ.length), h("blockquote", {}, s.m[L]), h("h3", {}, t().q));
  const fb = h("div"); const nextBtn = h("button", {class: "btn", type: "button", hidden: "", onclick: () => { if (q.i + 1 >= QUIZ.length) q.done = true; else { q.i++; } q.answered = false; render(); }}, q.i + 1 >= QUIZ.length ? t().finish : t().next2);
  s.o[L].forEach((txt, i) => { const b = h("button", {class: "opt", type: "button"}, txt);
    b.addEventListener("click", () => { if (q.answered) return; q.answered = true; if (i === s.c) q.score++;
      card.querySelectorAll(".opt").forEach((o, j) => { o.disabled = true; if (j === s.c) o.classList.add("ok"); else if (j === i) o.classList.add("no"); });
      fb.replaceChildren(h("p", {}, h("strong", {}, i === s.c ? t().right : t().wrong), " " + s.w[L]), h("p", {class: "warn"}, h("strong", {}, t().tip + ": "), s.t[L])); nextBtn.hidden = false; });
    card.append(b); });
  card.append(fb, nextBtn); v.append(card);
}
async function pResources(v) {
  v.append(h("h1", {}, t().resH), h("p", {class: "warn"}, t().resNote)); const box = h("div"); v.append(box);
  try { const r = await api("/api/resources");
    box.append(...r.resources.map(x => h("div", {class: "card"}, h("strong", {}, x.name[st.lang]), h("p", {}, x.use[st.lang]),
      x.phone ? h("p", {}, t().call + ": " + x.phone) : null,
      x.url ? h("a", {href: x.url, target: "_blank", rel: "noopener noreferrer"}, t().open + " ↗ (" + x.url.replace(/^https?:\/\//, "") + ")") : null,
      h("p", {class: "note"}, "⚠ " + t().vstat))));
  } catch (e) { box.append(h("div", {class: "err"}, e instanceof TypeError ? t().net : e.message)); }
}
function pPrivacy(v) {
  v.append(h("h1", {}, t().privH), h("div", {class: "card"}, h("ul", {}, t().priv.map(p => h("li", {}, p)))), h("div", {class: "card"}, h("h2", {}, t().aboutH), h("p", {}, t().about), h("p", {class: "note"}, t().disc)));
}
document.getElementById("l-en").addEventListener("click", () => setLang("en"));
document.getElementById("l-hi").addEventListener("click", () => setLang("hi"));
window.addEventListener("hashchange", () => { const p = location.hash.slice(1); if (S.en.nav[p] && p !== st.page) { st.page = p; render(); } });
{ const p = location.hash.slice(1); if (S.en.nav[p]) st.page = p; }
render();
