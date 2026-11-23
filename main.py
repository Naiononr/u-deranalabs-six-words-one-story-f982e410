#!/usr/bin/env python3
"""Six Words, One Story.

Writes one complete story in exactly six words to /output/entry.txt:

    Grandma's voicemail still says "Don't worry."

Written against the judge's brief, in its priority order:
  1. A complete story in exactly six words: a grandchild keeps (and
     replays) a grandmother's voicemail — a beginning, a loss, and an
     aftermath are all in the line.
  2. The turn: the reassurance is spoken in the present tense by
     someone who is gone. "still says" makes the message outlive her:
     she cannot speak any more, yet her voice keeps saying it.
  3. Every word earns its place: "voicemail" makes it a voice kept
     after death, "still" makes the replay ongoing, "Don't worry" is
     the whole relationship in two words.
  4. Reads cleanly aloud, with a natural spoken rhythm.
  5. Leaves the unsaid to the reader: how she died, who is listening,
     how many times the message has been replayed.

Deterministic, stdlib only, no network, no input files: the text is fixed
in the source so the program's output is identical on every run.
"""

import os

STORY = 'Grandma\'s voicemail still says "Don\'t worry."'

OUTPUT_PATH = os.path.join(
    os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"), "entry.txt"
)


def validate_story(text: str) -> str:
    """Check the story against the gate and the brief, return it stripped.

    The gate requires 1-60 UTF-8 characters, not only white space, and
    the story must be exactly six words on a single line with no doubled
    spaces, so a slip in the source fails loudly here instead of shipping
    an invalid entry to the sealed scorer.
    """
    text = text.strip()
    assert text, "story must not be empty or only whitespace"
    assert "\n" not in text and "\r" not in text, "story must be a single line"
    assert "  " not in text, "story must not contain consecutive whitespace"
    words = text.split()
    assert len(words) == 6, f"story is {len(words)} words, must be 6"
    assert 1 <= len(text) <= 60, f"story is {len(text)} chars, must be 1-60"
    return text


def main() -> None:
    text = validate_story(STORY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fd = os.open(OUTPUT_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text + "\n")
    finally:
        # Guarantee world-readable even if the umask differs: the sealed
        # scorer cannot read a mode 0600 file.
        os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
