import json

from bbeval.graders.rules import (check_betting, check_emojis, check_headline,
                                  check_numbers_v1, check_numbers_v2, check_question)

CASES = {c["id"]: c for c in map(json.loads, open("data/cases.jsonl"))}


def test_hashtag_numbers_are_ignored():
    case = CASES[46]                     # "#49ers" used to be flagged as a stat
    assert not check_numbers_v1(case["gold_caption"], case["facts"])[0]
    assert check_numbers_v2(case["gold_caption"], case["facts"])[0]


def test_derived_odds_are_allowed():
    case = CASES[19]                     # "loses more than 4 times in 10" from 57%
    assert check_numbers_v2(case["gold_caption"], case["facts"])[0]


def test_singular_time_is_allowed():
    facts = {"win_probability": "81%"}   # the bug you found: "1 time in 5"
    assert check_numbers_v2("An 81% favorite loses about 1 time in 5.", facts)[0]


def test_invented_number_is_flagged():
    facts = {"win_probability": "57%"}
    passed, detail = check_numbers_v2("The Dodgers have won 12 straight at 57%.", facts)
    assert not passed
    assert "12" in detail


def test_betting_words_match_whole_words_only():
    assert check_betting("Who wins between these two?")[0]
    assert not check_betting("Lock this parlay in")[0]


def test_headline_allows_exactly_six_words():
    assert check_headline("One two three four five six")[0]
    assert not check_headline("One two three four five six seven")[0]


def test_emoji_limit():
    assert check_emojis("Great game ⚾ 📊")[0]
    assert not check_emojis("⚾⚾⚾⚾ too many")[0]


def test_question_rule():
    assert check_question("Who wins tonight?")[0]
    assert not check_question("Who wins tonight.")[0]

