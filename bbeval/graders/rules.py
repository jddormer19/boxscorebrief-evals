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



