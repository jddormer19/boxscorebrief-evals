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
- Locally, a long prompt will cost time whereas with an API they mostly cost money. When running, 35 of the 1.5B's 49 seconds went to reading the 1,516-token prompt. 
- There is a size threshold for reading structured data. Going from 3B to 7B, factor directions went from 1/4 to 4/4 and invented claims disappeared.
- The 3B was most dangerous because it had the right format and number but wrong facts. It looks convincing.
- We used a cached prompt with the 3B so its time can't be compared with the cold runs.

## Next (Friday)
- the free 7B writes, rule graders check, and the failures will get sent to claude
