import csv
import json
from pathlib import Path

from bbeval.graders.judge import judge

CASES = {c["id"]: c for c in map(json.loads, open("data/cases.jsonl"))}
LABELS = list(csv.DictReader(open("data/labels.csv", encoding="utf-8")))
OUT = Path("results/judge_calibration.jsonl")


def kappa(human, model):
    """Cohen's kappa: agreement between two lists of labels, corrected for chance."""
    n = len(human)
    observed = sum(h == m for h, m in zip(human, model)) / n
    categories = set(human) | set(model)
    expected = sum((human.count(k) / n) * (model.count(k) / n) for k in categories)
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def run_judge():
    """Judge every labeled case once and save the verdicts, so we only pay once."""
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w") as f:
        for row in LABELS:
            case = CASES[int(row["id"])]
            v = judge(case["gold_headline"], case["gold_caption"], case["facts"])
            f.write(json.dumps({"id": case["id"], **v.model_dump()}) + "\n")
            print(f"  #{case['id']}: judge q={v.quality} you q={row['quality']}")


def report():
    verdicts = {v["id"]: v for v in map(json.loads, OUT.open())}
    h_fact = [r["factual"] == "Y" for r in LABELS]
    m_fact = [verdicts[int(r["id"])]["factual"] for r in LABELS]
    h_q = [int(r["quality"]) for r in LABELS]
    m_q = [verdicts[int(r["id"])]["quality"] for r in LABELS]
    n = len(LABELS)
    print(f"factual agreement: {sum(a == b for a, b in zip(h_fact, m_fact))}/{n}")
    print(f"quality exact:     {sum(a == b for a, b in zip(h_q, m_q))}/{n}")
    print(f"quality within 1:  {sum(abs(a - b) <= 1 for a, b in zip(h_q, m_q))}/{n}")
    print(f"quality kappa:     {kappa(h_q, m_q):.2f}")
    print("disagreements (id: you -> judge):")
    for r, a, b in zip(LABELS, h_q, m_q):
        if a != b:
            print(f"  #{r['id']}: {a} -> {b}  {verdicts[int(r['id'])]['reason'][:100]}")


if __name__ == "__main__":
    if not OUT.exists():
        run_judge()
    report()
