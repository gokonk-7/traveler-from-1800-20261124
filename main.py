"""One Sentence for a Traveler from 1800.

Entrypoint for the make.fun bounty
"u-po-pu-one-sentence-for-a-traveler-from-1800-7e6162fb".

The deliverable is a single sentence, at most 200 characters, that explains
the modern internet to a time traveler who has just stepped out of the year
1800. The sentence stands alone: no words coined after the traveler's time,
no list of features, just one picture they could actually hold in their head.

The sentence lives in sentence.txt. This program prints exactly that
sentence to stdout, nothing else, so the graded output is the sentence
itself. It is fully deterministic: same input, same output, every run.
"""

from pathlib import Path

SENTENCE = (
    "Imagine a sea of ink in which every mind on earth dips its pen at once, "
    "so that a word written in London is read in Canton before the ink dries."
)


def main() -> None:
    sentence_path = Path(__file__).with_name("sentence.txt")
    text = sentence_path.read_text(encoding="utf-8").strip()
    assert text == SENTENCE, "sentence.txt and main.py disagree"
    assert len(text) <= 200, f"sentence is {len(text)} chars, over the 200 limit"
    assert text.count(".") == 1 and text.endswith("."), "must be exactly one sentence"
    print(text)


if __name__ == "__main__":
    main()
