
---
name: boxscorebrief-writer
description: Write a @boxscorebrief Instagram post from a case's facts, self-check it with the bbeval rule graders, and revise.
version: 1.0.0
author: jddormer19
platforms: [linux]
---

# boxscorebrief writer

Use when asked to write a post for a case id in ~/boxscorebrief-evals. All commands run from that folder.

## Steps
1. Read the post's kind and facts (only these; never look at old captions in data/):
   `.venv/bin/python -m bbeval.show_case <id>`
2. Read `prompts/v2.txt` and follow its rules exactly for this post's kind.
3. Write `drafts/<id>.json` with keys: headline, caption (no hashtags, no footer), hashtags (list, no # symbol), facts (copied from the case).
4. Check it: `.venv/bin/python -m bbeval.check_draft drafts/<id>.json`
5. If any check failed, revise the draft and check again, at most 2 revisions.
   A "numbers" failure can be a false alarm. If the number is a count of items in the facts, correct simple math from the facts,
   or a percentage stored as a decimal (0.357 = 35.7%), keep it and say why.
6. Reply with the final headline and caption, then one line: which checks failed on the first draft, and which (if any) still fail.

Never publish anything. This skill only writes drafts.
