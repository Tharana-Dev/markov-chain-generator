from collections import Counter, defaultdict, namedtuple, deque
import random
from typing import Optional
from itertools import pairwise
from functools import cache
import time

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
        for current, next_word in pairwise(sentence):
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
        return 
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

def collect_words(chain: dict, word: str) -> set[str]:
    """
    Finds all words reachable from the starting word.

    our new code creates one master set at the very beginning (visited). The inner function acts like a scout running through a maze.
    Every time the scout enters a new room (a new word), it prints the name of the word straight into that single master ledger (visited.add).
    It doesn't need to return anything because everything is stored in that shared container.
    """
    visited: set[str] = set()

    def dfs_collect_words(current_word: str):
        """
        base case: the word is already visited and added to the set -> bare return
        leap: for each word i trust the function to find all its pointing words
        """
        if current_word in visited:
            return
        visited.add(current_word)
        for upcoming_word in chain.get(current_word, {}):
            dfs_collect_words(upcoming_word)

    dfs_collect_words(word)
    return visited


def find_path(chain: dict, start: str, target: str) -> list[str] | None:
    """
    Finds a valid path from a start word to a target word in the Markov chain graph.

    This function utilizes a public-facing wrapper pattern that hides the complex 
    state-tracking mechanics of the underlying Depth-First Search (DFS) algorithm 
    from the external user API.

    Algorithm Mechanics:
        1. Shared State: Initializes a local `visited` set to track traversed nodes 
           and prevent infinite cyclic loops, a dynamic `current_path` list acting 
           as a live breadcrumb trail, and a `final_path` variable to capture the result.
        
        2. Backtracking Exploration: The nested inner scout (`dfs`) steps into 
           a word room, appending it to the trail. It systematically evaluates 
           every outward edge (follower word). 
           
        3. Incident Handling (Dead Ends vs. Success):
           - Dead Ends: If a word path yields no routes to the target, the algorithm 
             executes a backtracking operation via `.pop()`, slicing the erroneous 
             word off the trail to keep the history clean before returning `False`.
           - Success: When the target is discovered, a static array snapshot is 
             taken (`current_path + [target]`), and a `True` signal dominoes back up 
             the execution stack to instantly cease further graph exploration.

    Args:
        chain (dict): A dictionary representation of the text graph transition map.
        start (str): The starting word token to initiate traversal from.
        target (str): The destination word token being searched for.

    Returns:
        list[str] | None: An ordered sequence of words representing a valid path 
                          from start to target, or None if no path exists.
    """

    visited = set()
    current_path:list[str] = []
    final_path = None  # To store our successful snapshot

    def dfs(current_word: str) -> bool:
        """
            Base Case 1: If the word matches the target, we found it! We record our success and stop.
            Base Case 2: If the word is already visited, we skip it.

            leap:for each starter i trust the function to give the path from start to target
        """
        nonlocal final_path

        if current_word == target:
            final_path = current_path + [target]
            return True

        if current_word in visited:
            return False

        visited.add(current_word)
        current_path.append(current_word)  # Step into the room

        for follower in chain.get(current_word, []):
            if follower in visited:
                continue
            if dfs(follower) == True:
                return True

        current_path.pop()  # Backtrack: Step out of the room if it was a dead end
        return False

    dfs(start)
    return final_path

#study tip: we can't directly use @cache here because dictionaries are un hashable
#so we are using a cache function inside the main function
def shortest_path_cached(chain, start, target):
    """Same as shortest_path, but caches results across calls."""
    @cache
    def _cached_bfs(s, t):
        return shortest_path(chain, s, t)

    return _cached_bfs(start, target)
