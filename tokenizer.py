BODY_ABBREVIATIONS = {'mr', 'mrs', 'ms', 'dr', 'prof', 'st'}
END_ABBREVIATIONS = {'etc', 'al', 'approx', 'ibid'}
STRIP_PUNCS = '.,!?;:"()“”‘’'
SENTENCE_ENDS = {'.', '!', '?'}

def find_next_word_is_capitalized(text: str) -> list[bool]:
    """Returns a flat list of booleans corresponding to each word in text."""
    words = text.split()
    results = []
    
    for i in range(len(words)):
        if i + 1 < len(words):
            # Safe check in case the next word is just empty spaces
            next_word = words[i+1]
            next_is_capitalized = next_word[0].isupper() if next_word else False
            results.append(next_is_capitalized)
        else:
            results.append(False)
            
    return results


def tokenize_text(text: str) -> list[list[str]]:
    current_sentence: list[str] = []
    sentences: list[list[str]] = []

    capitalization_list = find_next_word_is_capitalized(text)

    for idx,raw in enumerate(text.split()):
        is_next_capitalized = capitalization_list[idx]

        cleaned = raw.lower().strip(STRIP_PUNCS)
        # SECONDARY PASS: Catches deeply nested contractions or secondary quotes
        cleaned = cleaned.strip(STRIP_PUNCS)
        
        if cleaned:
            current_sentence.append(cleaned)

        if raw[-1] in SENTENCE_ENDS and cleaned not in BODY_ABBREVIATIONS and (cleaned not in END_ABBREVIATIONS or is_next_capitalized):
# This ensures standalone punctuation (like "!") still triggers a sentence split
# Check if it's a sentence end, but skip if the cleaned word is an abbreviation
# Split if it ends in punctuation, unless it's a body abbreviation or an uncapitalized end abbreviation
# NLP Rule: Split on ending punctuation, skipping mid-sentence titles (like Dr.), 
# but forcing a split on end abbreviations (like etc.) if the next word is capitalized.

            if current_sentence:
                sentences.append(current_sentence)
            current_sentence = []

    if current_sentence:
        sentences.append(current_sentence) # to avoid missng the last sentence if no punctuation is given
    return sentences