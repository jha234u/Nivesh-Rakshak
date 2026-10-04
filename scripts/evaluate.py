"""Evaluate the rule engine on dataset/samples.csv. Run: python scripts/evaluate.py
Positive prediction = 'moderate_concern' or 'high_concern'. Ambiguous rows are listed but excluded from metrics."""
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
from app.analyzer import analyze_message

rows = list(csv.DictReader(open(ROOT / "dataset" / "samples.csv", encoding="utf-8")))
tp = fp = tn = fn = 0
misses, falarms = [], []
print(f"{'id':5}{'label':12}{'predicted':20}score")
for r in rows:
    res = analyze_message(r["message_text"], "en")
    pred_pos = res["result_category"] in ("moderate_concern", "high_concern")
    print(f"{r['sample_id']:5}{r['category']:12}{res['result_category']:20}{res['risk_score']}")
    if r["category"] == "suspicious":
        tp += pred_pos; fn += (not pred_pos)
        if not pred_pos: misses.append(r["sample_id"])
    elif r["category"] == "legitimate":
        fp += pred_pos; tn += (not pred_pos)
        if pred_pos: falarms.append(r["sample_id"])
div = lambda a, b: (a / b) if b else float("nan")
p, rc = div(tp, tp + fp), div(tp, tp + fn)
f1 = div(2 * p * rc, p + rc)
print(f"\nN (excluding ambiguous) = {tp+fp+tn+fn}   confusion: TP={tp} FP={fp} TN={tn} FN={fn}")
print(f"precision={p:.2f} recall={rc:.2f} F1={f1:.2f} false-positive-rate={div(fp, fp+tn):.2f}")
print("missed suspicious:", misses or "none"); print("false alarms:", falarms or "none")
print("\nCAVEAT: tiny, author-written dataset, tuned alongside the rules. Not a measure of real-world performance.")
