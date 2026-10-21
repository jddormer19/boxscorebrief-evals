import json
import sys

from bbeval.graders.rules import (check_betting, check_emojis, check_headline,
                                  check_length, check_numbers_v2, check_question)


def main(path):
    draft = json.load(open(path))
    caption, facts = draft["caption"], draft["facts"]
    checks = {
        "numbers": check_numbers_v2(caption, facts),
        "length": check_length(caption),
        "question": check_question(caption),
        "headline": check_headline(draft["headline"]),
        "emojis": check_emojis(caption),
        "betting": check_betting(caption),
    }
    failed = {name: why for name, (ok, why) in checks.items() if not ok}
    print(json.dumps({"passed": not failed, "failed": failed}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
