import json
import sqlite3
from pathlib import Path

DB = Path.home() / "insta-stats/data/insta_stats.sqlite3"
OUT = Path(__file__).resolve().parent.parent / "data/cases.jsonl"
TEST_START = "2026-10-18"            # dev = posts before this date
FRESH_START = "2026-10-21T18:00"     # fresh = posts created after the harness was built

def load_posts():
    conn = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM posts ORDER BY created_at").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def to_case(row):
    facts = json.loads(row["facts"])
    if not facts:
        return None #nothing to evaluate (e.g welcome post)
    return {
        "id": row["id"],
        "kind": row["kind"],
        "created_at": row["created_at"],
        "facts": facts,
        "gold_headline": row["headline"],
        "gold_caption": row["caption"],
        "status": row["status"],
        "flags": row["flags"],
        "has_flags": bool(row["flags"])
        }

def main():
    cases = [c for c in (to_case(r) for r in load_posts()) if c]
    for c in cases:
            if c["created_at"] < TEST_START:
                    c["split"] = "dev"
            elif c["created_at"] < FRESH_START:
                    c["split"] = "test"
            else:
                    c["split"] = "fresh"    

    OUT.write_text("".join(json.dumps(c) + "\n" for c in cases))
    print(f"wrote {len(cases)} cases to {OUT}") 
    for split in ("dev", "test", "fresh"):
        part = [c for c in cases if c["split"] == split]
        statuses = {}
        for c in part:
            statuses[c["status"]] = statuses.get(c["status"], 0) + 1
        print(f"  {split}: {len(part)} cases, {statuses}")


if __name__ == "__main__":
    main()
