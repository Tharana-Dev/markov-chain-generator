from collections import Counter, defaultdict, namedtuple
import random
ChainData = namedtuple("ChainData", ["sentences", "starts", "chain"])


def get_starters(sentences) -> Counter[str]:
    return Counter(sentence[0] for sentence in sentences if sentence)

def build_chain(sentences: list[list[str]]) -> defaultdict[str, Counter]:
    """
    args:
        list of sentences, each a list of words.
    returns:
        a defaultdict(Counter) where:
            key = a word
            value = Counter of words that follow it
    complexity: O(n)
    """

    chain: defaultdict = defaultdict(Counter)

    for sentence in sentences:
        for current, next_word in zip(sentence, sentence[1:]):
            chain[current][next_word] += 1

    return chain


def get_data(sentences: list[list[str]]) -> ChainData:
    chain = build_chain(sentences)
    starts = get_starters(sentences)

    return ChainData(sentences=sentences, starts=starts, chain=chain)

def weighted_pick(counter: Counter) -> str:
    """Pick a random key from the Counter, proportional to its count."""
    return random.choices(
        population=list(counter.keys()),
        weights=list(counter.values()),
        k=1
    )[0]

def generate(data: ChainData, start: str |None  = None, length: int = 20) -> list[str]:
    if length <=0 or not data.starts:
        return []
    if start is None:
        start = weighted_pick(data.starts)

    result:list[str] = [start]
    current = start
    for _ in range(length - 1):
        followers = data.chain.get(current)
        if not followers:
            break
        current = weighted_pick(followers)
        result.append(current)

    return result


if __name__ == "__main__":
    from tokenizer import tokenize_text
    import random

    data = get_data(tokenize_text("The cat sat. The dog ran. The cat ran. The dog sat. he. she. it. they"))
    result = generate(data,'the',10)

    print(result)