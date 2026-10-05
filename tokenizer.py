RIGHT_STRIP_PUNCS = ".,!?;:"
SENTENCE_ENDS = ".!?"


def tokenize_text(text: str) -> list[list[str]]:
    """
    Split text into sentences, each sentence a list of clean words.

    Cleaning per word: lowercase, then strip trailing punctuation.
    A sentence ends when a raw token finishes with . ! or ?

    Examples:
        "The cat sat. The dog ran!" ->
            [["the", "cat", "sat"], ["the", "dog", "ran"]]

    Complexity: O(C) where C = len(text).
    """

    sentences: list[list[str]] = []
    current:list[str] = []

    for raw_word in text.split():
        cleaned = raw_word.lower().rstrip(RIGHT_STRIP_PUNCS)
        if cleaned:
            current.append(cleaned)
            if raw_word[-1] in SENTENCE_ENDS:
                if current:
                    sentences.append(current)
                current = []

    if current:
        sentences.append(current)

    return sentences



