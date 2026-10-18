# Markov Chain Text Generator & Graph Engine

A robust, dependency-free Python implementation of an Order-1 Markov chain text generator and graph traversal engine. It tokenizes corpora with intelligent sentence boundary detection, builds a statistical model of token transitions, and provides tools for probabilistic generation and multi-hop graph pathfinding.

## Features

- **Zero External Dependencies** — Engineered using exclusively standard library components (`collections`, `random`, `itertools`, `functools`).
- **NLP Look-Ahead Tokenizer** — Handles mid-sentence structural titles (`Mr.`, `Dr.`) without triggering false sentence breaks, while correctly resolving standalone punctuation and context-aware end abbreviations (`etc.`).
- **Memory-Optimized Processing** — Graph generation loops use `itertools.pairwise` for $O(n)$ time complexity, avoiding redundant array allocation memory slices.
- **Lazy Evaluation Engine** — Features a structural generator stream utilizing `yield` pipelines for safe memory scaling and instant early exits.
- **Graph Traversal Toolkit** — Equipped with cycle-preventing Depth-First Search (DFS) for structural footprint analysis, deterministic Backtracking Route Discovery, and Breadth-First Search (BFS) for literal shortest-path optimization.
- **Performance Caching** — Uses `functools.cache` via a closure to memoize expensive BFS pathfinding queries, returning identical paths instantly on subsequent calls.
- **Persistent Historical Logging** — Runtime output pipelines utilize memory-efficient list buffers to seamlessly write and append dynamic string data to persistent local logs (`output.txt`) alongside a chronological real-time tracking engine.

## Project Structure

```
.
├── chain.py       # Transition network modeling, streaming logic, and graph algorithms
├── tokenizer.py   # Look-Ahead text processing and regex-free configuration boundaries
├── main.py        # Demo suite running model evaluation on cross-genre data structures
├── sample_text.txt# Sample corpus used for the demo
└── tests/         # Pytest suite covering tokenizer, chain building, and traversals
```

## Architecture

![Project Screenshot](diagram.png)


This project is split into distinct processing stages: text ingestion, tokenization, model building, generation, and graph search. The demo orchestrates these modules, pushing results to both the terminal and a historical log.

### System Data Flow (22/22 Connections Verified)
- **User → Demo Orchestrator:** `main.py` handles execution.
- **Demo Orchestrator → Sample Corpus / Tokenizer:** Samples `sample_text.txt` and runs `tokenize_text`.
- **Tokenizer → Capitalization Look-ahead:** Checks casing to prevent false sentence splits.
- **Demo Orchestrator → Chain Data Builder:** Calls `build_chain`.
- **Chain Data Builder → Starter Frequencies / Transition Counts:** Populates the `defaultdict(Counter)`.
- **Demo Orchestrator → Text Generation / Lazy Generation:** Calls `generate` and `generate_stream`.
- **Text Generation → Weighted Selection:** Uses `random.choices` to pick the next token.
- **Demo Orchestrator → Reachability DFS / Backtracking DFS / Shortest-Path BFS:** Runs graph algorithms on the transition counts.
- **Shortest-Path BFS → Path Reconstruction:** Follows parent pointers to rebuild the shortest route.
- **Demo Orchestrator → Terminal / Historical Log:** Prints results and appends to `output.txt`.

## How It Works

### 1. Tokenization (`tokenizer.py`)
`tokenize_text` reads an index map of subsequent tokens. A sentence ends if a token finishes with punctuation (`.`, `!`, `?`), provided it is not explicitly blocked by title scopes or uncapitalized follow-ups.

```python
tokenize_text("Dr. Manette sat. The dog ran, etc. Then it left.")
# → [["dr", "manette", "sat"], ["the", "dog", "ran", "etc"], ["then", "it", "left"]]
```

### 2. Building the Memory-Safe Chain (`chain.py`)
`build_chain` maps adjacent nodes efficiently without copying objects using `itertools.pairwise`:
```python
from itertools import pairwise

for current, next_word in pairwise(sentence):
    chain[current][next_word] += 1
```
This produces an optimized `defaultdict(Counter)` model payload.

### 3. Pathfinding & Search Theory
The network is mapped as a directed graph:
- **DFS Pathfinding:** Explores path sequences recursively via backtracking, using a state ledger to dynamically append and `.pop()` dead ends.
- **BFS Shortest Path:** Employs a double-ended queue (`deque`) to iteratively extract paths containing the absolute minimum edge hops possible.
- **Cached BFS:** Wraps the BFS in a closure using `@cache` so identical `(start, target)` queries run in O(1) time after the first call.

## Example Output

Since `output.txt` changes with every run, here is a static example of what the `main.py` demo produces:

```text
--- Generated Texts ---
the city is the end everything below
the ocean also feeds us forward and nutrients

--- Graph Traversal Demos ---
DFS path from 'into' to 'brown': ['into', 'it', 'is', 'a', 'considerable', 'difference', 'to', 'you', 'lestrade', 'drawled', 'holmes', 'before', 'his', 'rival', 'vanished', 'i', 'will', 'keep', 'the', 'light', 'brown']
BFS path from 'into' to 'brown': ['into', 'it', 'the', 'light', 'brown']

BFS path 1 (Calculated): ['door', 'that', 'came', 'a', 'marriage', 'also—but']
  └─ Duration: 0.00076430 seconds
BFS path 2 (Cached Hit): ['door', 'that', 'came', 'a', 'marriage', 'also—but']
  └─ Duration: 0.00054670 seconds
  └─ Performance: Second call was 1.40x faster!

--- Generator Demo (Lazy Stream) ---
First 10 words from an infinite-ish generator:
  your
  experience
  you
  are
  faddy
  people
```

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
| | `shortest_path_cached(...)` | Wraps `shortest_path` with `@cache` for O(1) repeat queries. |

## Usage

### Running the Validation Environment
Execute the validation module to verify data parsing pipelines, benchmark path discovery, and output model string mashups:
```bash
python main.py
```

### Programmatic Integration
```python
from tokenizer import tokenize_text
from chain import get_data, generate, shortest_path_cached

corpus = "Your text data goes here..."
data = get_data(tokenize_text(corpus))

# Execute a weighted structural text generation
print(" ".join(generate(data, length=30)))

# Find the absolute shortest thematic bridge between isolated nodes
path = shortest_path_cached(data.chain, start="alice", target="key")
print(f"Optimal path: {path}")
```

## Notes & Known Limitations

- **Order-1 Markov Horizon:** The transition matrix looks only at the immediately preceding word. This yields strong local grammatical pairings but lacks macro text coherence over long sentences. 
- **No Vocabulary Smoothing:** The model can only transition between exact word pairings encountered during training. If the generator lands on a terminal leaf node (dead end), generation halts early.
- **Normalization Artifacts:** The tokenizer strips all casing and text punctuation to optimize the mathematical graph connections. Re-casing and adding structural grammar formatting to generated text must be handled as a downstream layer.
- **Call-Stack Depth:** The internal graph search functions (`collect_words` and `find_path`) utilize recursion. Processing exceptionally massive textual corpora may hit system limits (`RecursionError`). For industrial workloads, an iterative stack implementation is recommended.

## License
Public domain / MIT — do whatever you like with it.
