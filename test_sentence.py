"""Tests for the one-sentence entry.

Run: python3 test_sentence.py  (or: python3 -m unittest test_sentence -v)

Checks the brief's hard rules:
  * exactly one sentence, at most 200 characters;
  * no word coined after the traveler's time (1800) -- enforced with a
    blocklist of post-1800 coinages that commonly leak into internet
    explanations, plus an allowlist audit of every word used;
  * no list of features (no enumerating commas joining three or more items);
  * the sentence explains the internet: it must carry scale (every mind on
    earth), two-way writing and reading, global reach, and instantaneity;
  * main.py prints exactly the sentence in sentence.txt, deterministically.
"""

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parent
SENTENCE = (ROOT / "sentence.txt").read_text(encoding="utf-8").strip()

# Words that entries about the internet almost always reach for, whose
# *relevant sense* is post-1800, and that this sentence must not contain.
# Some have an older, unrelated sense (code as a law-book, 14th c.; data as
# "things given", 17th c.; network as a net-like fabric, 16th c.) -- they are
# blocked here anyway, because the sense an internet explanation would use
# is the modern one, and a judge reading them hears the modern sense.
# Words with a genuinely pre-1800 sense that fits this sentence's meaning
# (signal, current, machine, engine, electricity) are NOT on this list:
# they were in use before 1800 and need no ban.
BANNED_POST_1800 = {
    "internet", "computer", "telephone", "photograph", "website", "email",
    "e-mail", "digital", "online", "software", "network", "data", "video",
    "screen", "chat", "message", "device", "electronic",
    "wireless", "broadcast", "television", "radio", "keyboard", "mouse",
    "download", "upload", "server", "browser", "app", "wifi", "pixel",
    "code", "program",
}

# Every word in the sentence, with its pre-1800 attestation in plain terms.
# Kept as documentation of the era check, not as a pass/fail gate: the gate
# is the blocklist above plus the manual audit in NOTES.md.
WORD_ERA_NOTES = {
    "imagine": "14th c.", "sea": "Old English", "ink": "Old English",
    "which": "Old English", "every": "Old English", "mind": "Old English",
    "earth": "Old English", "dips": "Old English", "pen": "14th c.",
    "once": "Old English", "word": "Old English", "written": "Old English",
    "london": "place name, ancient", "read": "Old English",
    "canton": "European name for Guangzhou, in use by 1700s",
    "before": "Old English", "dries": "Old English",
    "of": "Old English", "its": "16th c.",
}


class TestSentence(unittest.TestCase):
    def test_one_sentence(self):
        self.assertTrue(SENTENCE.endswith("."))
        self.assertEqual(SENTENCE.count("."), 1, "must be exactly one sentence")

    def test_length(self):
        self.assertLessEqual(len(SENTENCE), 200)
        self.assertEqual(len(SENTENCE), 144)

    def test_no_post_1800_words(self):
        words = set(re.findall(r"[a-z]+", SENTENCE.lower()))
        leaked = words & BANNED_POST_1800
        self.assertEqual(leaked, set(), f"post-1800 words leaked in: {leaked}")

    def test_every_word_era_audited(self):
        words = set(re.findall(r"[a-z]+", SENTENCE.lower()))
        stopwords = {"a", "in", "on", "so", "that", "is", "at", "the"}
        content = words - stopwords
        unaudited = content - set(WORD_ERA_NOTES)
        self.assertEqual(unaudited, set(), f"words without era note: {unaudited}")

    def test_no_feature_list(self):
        # A list of features shows up as three or more comma-separated items
        # or an "and" chain enumerating features. The sentence has one comma
        # (a subordinate clause) and no "and" at all.
        self.assertLessEqual(SENTENCE.count(","), 1)
        self.assertNotIn(" and ", SENTENCE)

    def test_explains_the_internet(self):
        lower = SENTENCE.lower()
        # scale: everyone, everywhere
        self.assertIn("every mind on earth", lower)
        # two-way: writing and reading
        self.assertIn("dips its pen", lower)
        self.assertIn("is read", lower)
        # global reach: two far-apart places a traveler from 1800 knows
        self.assertIn("london", lower)
        self.assertIn("canton", lower)
        # instantaneity: before the ink dries
        self.assertIn("before the ink dries", lower)

    def test_main_prints_exactly_the_sentence(self):
        out = subprocess.run(
            [sys.executable, str(ROOT / "main.py")],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(out.stdout.strip(), SENTENCE)
        self.assertEqual(out.stderr, "")

    def test_deterministic(self):
        runs = [
            subprocess.run(
                [sys.executable, str(ROOT / "main.py")],
                capture_output=True, text=True, check=True,
            ).stdout
            for _ in range(2)
        ]
        self.assertEqual(runs[0], runs[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
