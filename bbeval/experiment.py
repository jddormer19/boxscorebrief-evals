import statistics
import time
import json
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

from bbeval.graders.judge import judge
from bbeval.graders.rules import (check_betting, check_emojis, check_headline,
                                  check_length, check_numbers_v2, check_question)

load_dotenv()
WRITER_MODEL = "claude-opus-5-5"   # the same model production uses
CASES = [c for c in map(json.loads, open("data/cases.jsonl")) if c["split"] == "test"]
client = anthropic.Anthropic()


class PostCopy(BaseModel):
    headline: str
    caption: str
    hashtags: list[str]

def write(prompt, kind, facts):
    """Write one post exactly the way insta-stats does, but with the given system prompt."""
    start = time.perf_counter()
    response = client.beta.messages.parse(
        model=WRITER_MODEL,
        max_tokens=16000,
        output_config={"effort": "low"},
        system=prompt,
        messages=[{"role": "user", "content": f"Post type: {kind}\nFacts:\n{json.dumps(facts, indent=2)}"}],
        output_format=PostCopy,
    )
    seconds = time.perf_counter() - start
    return response.parsed_output, response.usage, seconds


def rules_passed(copy, facts):
    """How many of the 6 rule graders this post passes."""
    checks = [
        check_numbers_v2(copy.caption, facts),
        check_length(copy.caption),
        check_question(copy.caption),
        check_headline(copy.headline),
        check_emojis(copy.caption),
        check_betting(copy.caption),
    ]
    return sum(passed for passed, _ in checks), len(checks)


def run(version):
    """Write + judge every test case with one prompt version, saving each result."""
    prompt = Path(f"prompts/{version}.txt").read_text()
    out = Path(f"results/experiment_{version}.jsonl")
    with out.open("w") as f:
        for case in CASES:
            copy, usage, seconds = write(prompt, case["kind"], case["facts"])
            verdict = judge(copy.headline, copy.caption, case["facts"])
            passed, total = rules_passed(copy, case["facts"])
            row = {
                "id": case["id"],
                "version": version,
                **copy.model_dump(),
                **verdict.model_dump(),
                "rules_passed": passed,
                "rules_total": total,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "write_seconds": round(seconds, 2),
            }
            f.write(json.dumps(row) + "\n")
            print(f"  {version} #{case['id']}: quality={verdict.quality} factual={verdict.factual} "
                  f"loser={verdict.loser_framing} rules={passed}/{total}")


def summary(version):
    rows = [json.loads(line) for line in open(f"results/experiment_{version}.jsonl")]
    n = len(rows)
    print(f"{version}: quality {sum(r['quality'] for r in rows) / n:.2f}"
          f" | factual {sum(r['factual'] for r in rows)}/{n}"
          f" | loser framing {sum(r['loser_framing'] for r in rows)}/{n}"
          f" | rules {sum(r['rules_passed'] for r in rows)}/{sum(r['rules_total'] for r in rows)}"
          f" | writer tokens in/out {sum(r['input_tokens'] for r in rows)}/{sum(r['output_tokens'] for r in rows)}")
    times = [r["write_seconds"] for r in rows if "write_seconds" in r]
    print(f"     median write time: {statistics.median(times):.1f}s" if times else "     median write time: n/a")


if __name__ == "__main__":
    versions = sys.argv[1:] or ["v1", "v2"]
    for v in versions:
        if not Path(f"results/experiment_{v}.jsonl").exists():
            run(v)
    for v in versions:
        summary(v)
