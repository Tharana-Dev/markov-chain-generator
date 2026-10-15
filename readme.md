# Markov Chain Text Generator & Graph Engine

A robust, dependency-free Python implementation of an Order-1 Markov chain text generator and graph traversal engine. It tokenizes corpora with intelligent sentence boundary detection, builds a statistical model of token transitions, and provides tools for probabilistic generation and multi-hop graph pathfinding.

## Features

- **Zero External Dependencies** — Engineered using exclusively standard library components (`collections`, `random`).
- **NLP Look-Ahead Tokenizer** — Handles mid-sentence structural titles (`Mr.`, `Dr.`) without triggering false sentence breaks, while correctly resolving standalone punctuation and context-aware end abbreviations (`etc.`).
- **Memory-Optimized Processing** — Graph generation loops use pointer indices (`range(len(sentence) - 1)`) to achieve $O(n)$ time complexity while avoiding redundant array allocation memory slices.
- **Lazy Evaluation Engine** — Features a structural generator stream utilizing `yield` pipelines for safe memory scaling and instant early exits.
- **Graph Traversal Toolkit** — Equipped with cycle-preventing Depth-First Search (DFS) for structural footprint analysis, deterministic Backtracking Route Discovery, and Breadth-First Search (BFS) for literal shortest-path optimization.
- **Persistent Historical Logging** — Runtime output pipelines utilize memory-efficient list buffers to seamlessly write and append dynamic string data to persistent local logs (`output.txt`) alongside a chronological real-time tracking engine.
## Project Structure

```
.
├── chain.py       # Transition network modeling, streaming logic, and graph algorithms
├── tokenizer.py   # Look-Ahead text processing and regex-free configuration boundaries
└── main.py        # Demo suite running model evaluation on cross-genre data structures
```

## How It Works

### 1. Tokenization (`tokenizer.py`)
`tokenize_text` reads an index map of subsequent tokens. A sentence ends if a token finishes with punctuation (`.`, `!`, `?`), provided it is not explicitly blocked by title scopes or uncapitalized follow-ups.

```python
tokenize_text("Dr. Manette sat. The dog ran, etc. Then it left.")
# → [["dr", "manette", "sat"], ["the", "dog", "ran", "etc"], ["then", "it", "left"]]
```

### 2. Building the Memory-Safe Chain (`chain.py`)
`build_chain` maps adjacent nodes efficiently without copying objects:
```python
for i in range(len(sentence) - 1):
    chain[sentence[i]][sentence[i + 1]] += 1
```
This produces an optimized `defaultdict(Counter)` model payload.

### 3. Pathfinding & Search Theory
The network is mapped as a directed graph:
- **DFS Pathfinding:** Explores path sequences recursively via backtracking, using a state ledger to dynamically append and `.pop()` dead ends.
- **BFS Shortest Path:** Employs a double-ended queue (`deque`) to iteratively extract paths containing the absolute minimum edge hops possible.

### 4. Continuous Audit Logging (`main.py`)
To monitor vocabulary scaling and pathway transformations over time, execution passes are buffered in memory and appended to `output.txt`. Every execution event writes a custom analytical record framed by structural demarcation dividers and real-time execution timestamps.

## API Reference

| Component | Signature | Description |
| :--- | :--- | :--- |
| **Tokenizer** | `find_next_word_is_capitalized(text: str) -> list[bool]` | Pre-computes look-ahead lookups for character capitalization casing. |
| | `tokenize_text(text: str) -> list[list[str]]` | Emits cleaned, non-overlapping nested token arrays. |
| **Markov** | `build_chain(sentences: list[list[str]]) -> defaultdict` | Evaluates adjacent sequences into weighted state distributions. |
| | `generate(data: ChainData, ...) -> list[str]` | Generates a fixed array up to maximum boundary restrictions. |
| | `generate_stream(data: ChainData, ...) -> Iterator[str]` | Lazily yields strings one-by-one with immediate bare exits. |
| **Graph** | `collect_words(chain: dict, word: str) -> set[str]` | Extracts complete downstream accessibility domains via hidden DFS. |
| | `find_path(chain: dict, start: str, target: str) -> list[str] \| None` | Backtracks deep branches to capture a safe structural path route. |
| | `shortest_path(chain: dict, start: str, target: str) -> list[str] \| None` | Uses a tracking queue to guarantee the shortest route between nodes. |

## Usage

### Running the Validation Environment
Execute the validation module to verify data parsing pipelines, benchmark path discovery, and output model string mashups:
```bash
python main.py
```

### Programmatic Integration
```python
from tokenizer import tokenize_text
from chain import get_data, generate, shortest_path

corpus = "Your text data goes here..."
data = get_data(tokenize_text(corpus))

# Execute a weighted structural text generation
print(" ".join(generate(data, length=30)))

# Find the absolute shortest thematic bridge between isolated nodes
path = shortest_path(data.chain, start="alice", target="key")
print(f"Optimal path: {path}")
```

## Notes & Known Limitations

- **Order-1 Markov Horizon:** The transition matrix looks only at the immediately preceding word. This yields strong local grammatical pairings but lacks macro text coherence over long sentences. 
- **No Vocabulary Smoothing:** The model can only transition between exact word pairings encountered during training. If the generator lands on a terminal leaf node (dead end), generation halts early.
- **Normalization Artifacts:** The tokenizer strips all casing and text punctuation to optimize the mathematical graph connections. Re-casing and adding structural grammar formatting to generated text must be handled as a downstream layer.
- **Call-Stack Depth:** The internal graph search functions (`collect_words` and `find_path`) utilize recursion. Processing exceptionally massive textual corpora may hit system limits (`RecursionError`). For industrial workloads, an iterative stack implementation is recommended.

## License
Public domain / MIT — do whatever you like with it.