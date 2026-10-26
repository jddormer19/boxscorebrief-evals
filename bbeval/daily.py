import statistics
import json
from datetime import date
from pathlib import Path

from bbeval.experiment import rules_passed, write
from bbeval.graders.judge import judge

OUT = Path("results/fresh.jsonl")
VERSIONS = ["v1", "v2"]


def scored_ids():
    """Ids of fresh posts already scored on an earlier day."""
    if not OUT.exists():
        return set()
    return {row["id"] for row in map(json.loads, OUT.open())}


def score(case, version):
    """Write, judge and rule-check one fresh post with one prompt version."""
    prompt = Path(f"prompts/{version}.txt").read_text()
    copy, usage, seconds = write(prompt, case["kind"], case["facts"])
    verdict = judge(copy.headline, copy.caption, case["facts"])
    passed, total = rules_passed(copy, case["facts"])
    return {
        "id": case["id"],
        "version": version,
        "scored_on": str(date.today()),
        **copy.model_dump(),
        **verdict.model_dump(),
        "rules_passed": passed,
        "rules_total": total,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "write_seconds": round(seconds, 2),
    }


def score_new():
    cases = [c for c in map(json.loads, open("data/cases.jsonl")) if c["split"] == "fresh"]
    done = scored_ids()
    new = [c for c in cases if c["id"] not in done]
    for case in new:
        rows = [score(case, v) for v in VERSIONS]   # both versions succeed before anything is saved
        with OUT.open("a") as f:
            f.writelines(json.dumps(row) + "\n" for row in rows)
    return new


def report(new):
    rows = [json.loads(line) for line in OUT.open()]
    print(f"boxscorebrief-evals daily: scored {len(new)} new fresh posts ({len(rows) // len(VERSIONS)} total)")
    for v in VERSIONS:
        rs = [r for r in rows if r["version"] == v]
        n = len(rs)
        print(f"{v}: quality {sum(r['quality'] for r in rs) / n:.2f}"
              f" | factual {sum(r['factual'] for r in rs)}/{n}"
              f" | loser framing {sum(r['loser_framing'] for r in rs)}/{n}"
              f" | rules {sum(r['rules_passed'] for r in rs)}/{sum(r['rules_total'] for r in rs)}")
        times = [r["write_seconds"] for r in rs if "write_seconds" in r]
        if times:
            print(f"    median write time: {statistics.median(times):.1f}s")

if __name__ == "__main__":
    new = score_new()
    if new:
        report(new)
