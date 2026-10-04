# Testing Report (actually executed, 2026-10-04, sandbox without internet)

## Executed
`python -m unittest discover -s tests -v` → **29 tests: 27 passed, 0 failed, 2 skipped**.
Skipped: `tests/test_fastapi.py` (FastAPI/httpx could not be installed offline). **The FastAPI layer has therefore never been run.**
Passed highlights: exact-substring evidence, negation (EN/HI), Hindi output, URL lookalike/IP/shortener/dangerous-scheme rejection, malformed JSON/oversize, rate limit, no temp files written, upload validation, a real Tesseract OCR round-trip on a generated English image, and live HTTP tests (security headers, path traversal blocked, Hindi API call).

## Evaluation (`python scripts/evaluate.py`)
Dataset: 25 fictional, author-written messages (12 suspicious, 10 legitimate, 3 ambiguous excluded from metrics). Positive = moderate/high concern.
Result: TP=9 FP=0 TN=10 FN=3 → precision 1.00, recall 0.75, F1 0.86, false-positive rate 0.00.
Misses (S10, S11, S12) are deliberate hard cases with no rule keywords (hype without keywords, indirect OTP request).
**Caveat:** rules and dataset were written by the same person; these numbers are optimistic and say nothing about real-world performance.

## Not tested
Real browser UI, mobile layout, Hindi OCR, any LLM path (not built), deployment, accessibility audit.
