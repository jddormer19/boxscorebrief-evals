import json
from pathlib import Path

from bbeval.experiment import CASES, PostCopy, rules_passed
from bbeval.graders.judge import judge

OUT = Path("results/experiment_hermes.jsonl")


def main():
    with OUT.open("w") as f:
        for case in CASES:
            draft = json.load(open(f"drafts/{case['id']}.json"))
            copy = PostCopy(headline=draft["headline"], caption=draft["caption"],
                            hashtags=draft.get("hashtags", []))
            verdict = judge(copy.headline, copy.caption, case["facts"])
            passed, total = rules_passed(copy, case["facts"])
            row = {
                "id": case["id"],
                "version": "hermes",
                **copy.model_dump(),
                **verdict.model_dump(),
                "rules_passed": passed,
                "rules_total": total,
                "input_tokens": 0,   # agent tokens are counted in Hermes's own logs instead
                "output_tokens": 0,
            }
            f.write(json.dumps(row) + "\n")
            print(f"  hermes #{case['id']}: quality={verdict.quality} factual={verdict.factual} "
                  f"loser={verdict.loser_framing} rules={passed}/{total}")


if __name__ == "__main__":
    main()

