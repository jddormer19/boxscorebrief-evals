import csv
import json

from bbeval.graders.rules import check_numbers_v1, check_numbers_v2

CASES = {c["id"]: c for c in map(json.loads, open("data/cases.jsonl"))}
LABELS = list(csv.DictReader(open("data/labels.csv", encoding="utf-8")))


def score(checker):
	false_alarms, missed, caught = [], [], []
	for row in LABELS:
		case = CASES[int(row["id"])]
		passed, _ = checker(case["gold_caption"], case["facts"])
		wrong = row ["factual"] == "N"
		if not passed and not wrong:
			false_alarms.append(case["id"])
		elif passed and wrong:
			missed.append(case["id"])
		elif not passed and wrong:
			caught.append(case["id"])
	return false_alarms, missed, caught


for name, checker in [("v1", check_numbers_v1), ("v2", check_numbers_v2)]:
	fa, miss, hit = score(checker)
	print(f"{name}: false alarms {len(fa)}/{len(LABELS)} missed {len(miss)} caught {len(hit)}")
	print(f"        false-alarm ids: {fa}")

