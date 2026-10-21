import json
import sys

case = next(c for c in map(json.loads, open("data/cases.jsonl")) if c["id"] == int(sys.argv[1]))
print(json.dumps({"kind": case["kind"], "facts": case["facts"]}, indent=2))
