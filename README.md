# NiveshRakshak AI 🛡️
**Your Smart Shield Against Digital Financial Scams** — SANGYAN hackathon (Track A: Digital Fraud & Scam Resilience, secondary Track E).

> NiveshRakshak AI is an educational safety-assistance prototype. Automated results are not definitive fraud determinations, legal advice, or investment recommendations. Verify important information using official sources.

## Problem and solution
Fake investment offers, phishing links and "guaranteed return" tips spread over WhatsApp and social media. First-time investors in smaller cities and regional-language communities often cannot judge them. NiveshRakshak AI shows **which warning signs appear, quotes the exact words, says how unsure it is, and explains safe next steps** in Hindi or English. It never gives stock tips, predicts returns or calls anything "confirmed fraud".

## What is implemented (and what is not)
| Feature | Status |
|---|---|
| Message analyzer (8 transparent rule groups, EN+HI, exact-substring evidence, negation handling) | Implemented, tested |
| URL analyzer (offline heuristics; never opens the link; no threat-intel lookup) | Implemented, tested |
| Screenshot analyzer (Tesseract OCR, in-memory, validated, 5 MB limit, graceful fallback) | Implemented, tested here (English OCR) |
| Hindi/English switcher (UI + analysis output; `S` dict in `frontend/app.js` and per-language tuples in backend are the extension points) | Implemented |
| Safety assistant (rule-based, refuses stock tips, warns on OTP sharing) | Implemented, offline only |
| Learning zone (5 scenarios, scoring) | Implemented |
| Resources page | Implemented, **links NOT live-verified** (see below) |
| Privacy: no storage of submissions, rate limit, CSP, input limits | Implemented (prototype level) |
| LLM explanations/translation | **Not implemented** (no network/API in the build environment). Core works without it. |
| React + Vite + Tailwind frontend | **Not used**: replaced by a dependency-free vanilla JS frontend (npm was unavailable) |
| Pitch deck, demo script, judge Q&A, PPTX, screenshots, deployment | **Not yet created** |

## Run it (no installs needed)
```bash
python backend/run_stdlib.py 8000      # open http://localhost:8000
```
FastAPI version (same logic, `backend/app/main.py` — **not executed in the build sandbox**):
```bash
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --port 8000
```
OCR needs the Tesseract binary; for Hindi OCR also install the `hin` language data (otherwise English OCR is used).

## API
`GET /api/health`, `GET /api/resources`, `POST /api/analyze/message` `{"text","language"}`, `POST /api/analyze/url` `{"url","language"}`, `POST /api/analyze/image` (raw image body, `Content-Type: image/png|jpeg|webp`), `POST /api/assistant/chat` `{"message","language"}`. Responses include `status, result_category, risk_score, detected_indicators, evidence, explanation, recommendations, uncertainty, language, disclaimer`.

Risk categories: `high_concern`, `moderate_concern`, `low_concern`, `no_known_patterns` (explicitly *not* "safe"), `insufficient_text`.

## Tests and evaluation
```bash
python -m unittest discover -s tests -v     # 29 tests
python scripts/evaluate.py                  # dataset/samples.csv
```
See `docs/TESTING_REPORT.md` for what was actually run and its limits.

## Known limitations
Keyword rules miss novel or indirect scams (3 deliberate "hard cases" in the dataset are missed) and can flag unusual genuine text. Hindi OCR was not tested. The frontend was syntax-checked and served over HTTP but **not exercised in a real browser**. Rate limiting is per-process memory. Resource entries were written from the author's knowledge, not live-checked.

## Privacy
No accounts, no database, no logs of submissions, images processed in memory. Only the language choice is kept in the browser. No OTPs/passwords are requested.
