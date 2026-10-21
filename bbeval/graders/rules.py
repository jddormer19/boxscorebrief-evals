import json
import re

FOOTER = "Follow for sports, by the numbers"


def split_caption(text):
    """Return just the body paragraphs, without the footer or hashtag lines."""
    paragraphs = text.split("\n\n")          # blank line = new paragraph
    body = []
    for p in paragraphs:
        p = p.strip()
        if p.startswith("#"):                # hashtag line -> skip
            continue
        if p.startswith(FOOTER):             # footer line -> skip
            continue
        body.append(p)
    return "\n\n".join(body)

def check_length(body):
    """Caption body must be under 900 characters."""
    n = len(body)
    if n < 900:
        return True, ""
    return False, f"too long: {n} chars"

def check_question(body):
    """Caption body must end with a question mark."""
    if body.strip().endswith("?"):
        return True, ""
    return False, "doesn't end with a question"

def check_headline(headline):
    """Headline must be at most 6 words."""
    words = headline.split()
    if len(words) <= 6:
        return True, ""
    return False, f"headline has {len(words)} words"

EMOJI = re.compile("[\U0001F000-\U0001FAFF\u2600-\u27BF]")


def check_emojis(body):
    """At most 3 emojis in the caption body."""
    found = EMOJI.findall(body)
    if len(found) <= 3:
        return True, ""
    return False, f"{len(found)} emojis: {''.join(found)}"

BETTING_WORDS = ["bet", "betting", "gamble", "gambling", "sportsbook",
                 "parlay", "spread", "moneyline", "units"]


def check_betting(body):
    """No betting language."""
    words = re.findall(r"[a-z]+", body.lower())
    hits = [w for w in words if w in BETTING_WORDS]
    if not hits:
        return True, ""
    return False, f"betting words: {', '.join(hits)}"


NUMBER = re.compile(r"\d+(?:\.\d+)?|\.\d+")

def facts_numbers(facts):
    """Every number that appears anywhere in the facts."""
    return set(NUMBER.findall(json.dumps(facts, ensure_ascii=False)))


def check_numbers_v1(body, facts):
    """The original insta-stats checker: flag numbers not found in the facts."""
    known = facts_numbers(facts)
    bad = sorted({n for n in NUMBER.findall(body) if n not in known}, key=float)
    if not bad:
        return True, ""
    return False, f"numbers not in facts: {', '.join(bad)}"


def check_numbers_v2(body, facts):
    """v2: like v1, but ignores hashtags and allows odds derived from percentages."""
    text = re.sub(r"#\w+", "", body)      # 1. remove hashtags like #49ers
    rates = known_rates(facts)
    for match in ODDS.finditer(text):           # 2. remove derived odds
            if is_derived(match.group(1), match.group(2), rates):
            	text = text.replace(match.group(0), "")    # 2. (next step) remove "4 in 10"-style odds that come from the facts
    return check_numbers_v1(text, facts)  # 3. run the original check on what's left

ODDS = re.compile(r"(\d+)\s+(?:times?\s+)?(?:in|out of)\s+(\d+)")

def known_rates(facts):
    """Every percentage in the facts as a 0-1 rate, plus its opposite (57% -> 0.57 and 0.43)."""
    rates = set()
    for n in facts_numbers(facts):
        x = float(n)
        if x <= 1:
            p = x            # already a rate, like 0.57
        elif x <= 100:
            p = x / 100      # a percent, like 57
        else:
            continue         # years, big totals: not a percentage
        rates.add(p)
        rates.add(1 - p)
    return rates

def is_derived(n, m, rates):
    """True if n/m is within 0.05 of a rate from the facts."""
    if int(m) == 0:
        return False         # can't divide by zero
    r = int(n) / int(m)
    return any(abs(r - p) <= 0.05 for p in rates)
