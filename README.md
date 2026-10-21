# boxscorebrief-evals

An evaluation harness for the AI that writes captions for [@boxscorebrief](https://instagram.com/boxscorebrief),
a live sports-by-the-numbers Instagram account. It measures caption quality with rule-based graders and a
calibrated LLM judge, then uses those measurements to improve the writer.

## Why

In order to keep the AI-written captions honestly, we need a way to measure the accuracy. To get the most accurate results, we chose to measure instead of just rely on eyeballing. We also want to keep the theme consitant throughout each caption.


## How it works
```mermaid
flowchart LR
    A[(Live posts DB<br/>53 posts)] --> B[Dataset<br/>date-based dev/test split]
    B --> C[Writer<br/>prompt v1 / v2 / Hermes agent]
    C --> D[Rule graders<br/>numbers, length, question,<br/>headline, emojis, betting]
    C --> E[LLM judge<br/>factual, loser framing, quality 1-5]
    H[30 hand labels] --> F[Calibration<br/>Cohen's kappa]
    E --> F
    D --> G[Results]
    E --> G
```

## Results

**1. The production number checker was mostly false alarms.**
| Checker | False alarms (of 30 labeled posts) |
|---|---|
| Original (v1) | 15 |
| Rebuilt (v2): ignores hashtags, allows odds derived from facts | **5** (−67%) |

There were no invented numbers in the labeled set, so the checker's recall is not yet tested (see Next steps).
We rejected three accurate posts due to false alarms.

**2. The LLM judge agrees with human labels at κ = 0.61.**
- First run: κ = 0.44. Reviewing the 9 disagreements showed the judge had caught **2 misread claims**
  (a wrong "biggest jump", a model adjustment described as a real scoring margin) that both the rule checker and I missed,
  and that 2 of my labels broke my own rubric. After adjudication: κ = 0.61, factual agreement 29/30.
- The judge also exposed a wrong human label (#41: a "35.7%" I thought was invented was in the facts as 0.357).
Both humans and LLM judges should both check themselves. It is always good to recheck each others work a few times.

**3. Eval-driven prompt fixes (16 test posts, same model, blind judge).**
| | Prompt v1 (production) | Prompt v2 |
|---|---|---|
| Captions framing our pick as a loser | 9/16 | **0/16** |
| Judge-flagged factual errors | 2/16 | **0/16** |
| Mean judge quality (1-5) | 3.38 | **4.81** |
| Writer input tokens | baseline | +5% |

We replaced the bad example which fixes the loser framing. Check claims and explained what model factors mean to fix wrong comparisons and invented reasoning.

**4. Hermes agent with self-check:** *results pending.*

## Limitations
- Small data: 53 posts, 30 hand-labeled by one person, one sample per caption.
- Test-set leakage: three errors that motivated prompt v2 came from test-set posts. Validation on new posts is in progress.
- The judge is stricter than I am on invented reasoning (it scores 1 where I score 2–4).
- Remaining checker false alarms (counts like "14 games", ratios like "20 times") need meaning, not rules.

## Run it
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install anthropic python-dotenv pytest
echo "ANTHROPIC_API_KEY=<your key>" > .env
python3 -m bbeval.dataset            # build data/cases.jsonl (needs the private posts DB)
python3 -m bbeval.compare_checkers   # checker v1 vs v2 against hand labels
python3 -m bbeval.calibrate          # judge vs hand labels, Cohen's kappa
python3 -m bbeval.experiment         # prompt v1 vs v2 on the test split
```

## Next steps
-vlaidating v2 on fresh posts via a daily Hermes job
-adversarial cases with planted fake stats to test recall
-CI
