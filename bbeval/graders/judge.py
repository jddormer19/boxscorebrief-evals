import json

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
JUDGE_MODEL = "claude-opus-5-5"

RUBRIC = """You grade Instagram captions for @boxscorebrief, a sports-by-the-numbers account.
You get the facts the writer was given and the caption it wrote. Grade strictly against the facts.

factual: true if every number and claim is supported by the facts. Count these as supported:
simple correct math from the facts (a 57% pick means the other side has 43%, roughly "4 in 10"),
counts of items in the facts ("14 games"), slide numbers, and hypothetical scores asked as a question.
false if any stat, record, or claim is invented, misread, or contradicts the facts.

loser_framing: true if, when describing uncertainty about an upcoming game, the caption describes
the model's own pick losing (e.g. "an 85% favorite still loses 3 times in 20"). Stating the other
team's chance in positive terms is fine (e.g. "Boston wins this 4 times in 10"). Reporting the real
results of games already played is never loser framing; owning misses is the account's brand.

quality 1-5. 5 = post as-is. 3 = needs edits. 1 = never post.
Any invented stat caps quality at 1. Loser framing caps quality at 3.

reason: one short sentence explaining the grade."""


class Verdict(BaseModel):
    factual: bool
    loser_framing: bool
    quality: int
    reason: str

client = anthropic.Anthropic()

def judge(headline, caption, facts, model=JUDGE_MODEL):
    """Ask Claude to grade one caption againts its facts. Returns a Verdict."""
    response = client.beta.messages.parse(
        model=model,
        max_tokens=1000,
        system=RUBRIC,
        messages=[{
            "role": "user",
            "content": f"Facts:\n{json.dumps(facts, indent=2)}\n\nHeadLine:{headline}\n\nCaption:\n{caption}",
        }],
        output_format=Verdict,
    )
    return response.parsed_output
