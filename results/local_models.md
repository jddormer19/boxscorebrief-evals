# Local model feasibility test (2026-10-26)

Same prompt for every model: prompt v2 + the facts for fresh post #59
(Cavaliers at 76ers, model pick PHI 55%, four factors, home team baseline 2.3).
Local models run with Ollama, 4-bit quantized Qwen 2.5.

| | Qwen 1.5B (laptop) | Qwen 3B (laptop) | Qwen 7B (Windows PC) | Claude + prompt v2 |
|---|---|---|---|---|
| Hardware | i5-5257U, 2 cores, ~2.8 GB free RAM | same | Core Ultra 7 155U, 12 cores, 32 GB RAM | API |
| Time per caption | 49s (cold) | 31s (warm cache)* | 77s (cold) | ~3s |
| Prompt reading speed | 43.6 tok/s | cached | 32.7 tok/s | - |
| Writing speed | 12.7 tok/s | 6.8 tok/s | 7.1 tok/s | - |
| Win probability (55%) included | no | yes | yes | yes |
| Factor directions correct | 0/4 | 1/4 | 4/4 | 4/4 |
| Invented claims | many | several (wrong home team, "recent struggles") | none | none |
| Rule misses | - | 1 | 2 (no closing question, 5 hashtags) | 0 |
| Cost per caption | $0 | $0 | $0 | fraction of a cent |

*The 3B run reused a cached prompt from an earlier run, so its time isn't comparable to the cold runs.

## What I learned
- ✍️ Where the time goes on a CPU (reading vs writing), and why prompt length matters more locally than with an API.
- ✍️ What changed between 3B and 7B, and what that says about choosing a model size.
- ✍️ Why the 3B caption was the most dangerous one even though it looked the best.
- ✍️ Why the comparison has to use the same conditions (cold vs warm).

## Next (Friday)
- ✍️ How you'll use the 7B in the LangGraph pipeline (hint: escalation).

Writing tips:
- Write like you'd say it to an interviewer: "On a CPU, most of the time went to..."
- Use a number in each line where you can (35 of 49 seconds, 0/4 → 4/4). Specific beats general.
