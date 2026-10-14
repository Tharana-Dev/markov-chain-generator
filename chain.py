from collections import Counter, defaultdict, namedtuple, deque
import random
from typing import Optional

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


def generate(data: ChainData, start: str | None = None, length: int = 20) -> list[str]:
    if length <= 0 or not data.starts:
        return []
    if start is None:
        start = weighted_pick(data.starts)

    result: list[str] = [start]
    current = start
    for _ in range(length - 1):
        followers = data.chain.get(current)
        if not followers:
            break
        current = weighted_pick(followers)
        result.append(current)

    return result

def generate_stream(data: ChainData, start: str | None = None, length: int = 20):
    if length <=0 or not data.starts:
        return []
    if start is None:
        start = weighted_pick(data.starts)

    yield start
    current = start
    for i in range(1, length):
        followers = data.chain.get(current)
        if not followers:
            return
        current = weighted_pick(followers)
        yield current


def rebuild_path(parent: dict[str, Optional[str]], target: str) -> list[str]:
    path = []
    current: Optional[str] = target
    while current is not None:
        path.append(current)
        current = parent.get(current)
    return path[::-1]


def shortest_path(graph: dict[str, Counter], start: str, target: str) -> Optional[list[str]]:
    """
    Uses BFS to return the shortest path.
    O(V + E) time, O(V) space. where v = vertices, e = edges
    """
    if start == target:
        return [target]

    visited = {start}
    queue = deque([start])
    parent: dict[str, Optional[str]] = {start: None}

    while queue:
        node = queue.popleft()
        neighbors = graph.get(node, {})

        for neighbor in neighbors.keys():
            if neighbor in visited:
                continue

            parent[neighbor] = node
            visited.add(neighbor)

            if neighbor == target:
                return rebuild_path(parent, target)

            queue.append(neighbor)

    return None

def collect_words(chain: dict, word: str, visited: set | None = None) -> set[str]:
    """
    base case : if the chain points to a word which is already there, return an empty set
    leap: if the word points out to some other element in the chain i collect all of them and add the word to it.
    """
    if visited is None:
        visited = set()
    if word in visited:
        return set()
    visited.add(word)
    result = {word}

    for upcoming_word in chain.get(word, {}):
        result |= collect_words(chain, upcoming_word, visited)

    return result


def find_path(chain: dict, start: str, target: str, visited: set | None = None) -> list[str] | None:
    """
    base case: start == target
    leap: 
        For each follower, I assume the recursive call finds a path from follower to target.
    """
    if visited is None: visited = set()

    if start == target:
        return [start]
    if start not in chain:
        return None

    visited.add(start)

    for follower in chain.get(start,[]):
        if follower in visited:
            continue
        path = find_path(chain, follower, target, visited)
        if path is not None:
            return [start] + path

    return None


if __name__ == "__main__":
    from tokenizer import tokenize_text
    import random

    data = get_data(tokenize_text(
        "The cat sat. The dog ran. The cat ran. The dog sat. he. she. it. they"))
    result = generate(data, 'the', 10)

    print(result)
