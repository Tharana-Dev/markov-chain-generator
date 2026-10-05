# Markov Chain Text Generator

A simple, dependency-free Python implementation of a Markov chain text generator. It tokenizes a body of text, builds a statistical model of word transitions, and generates new text by walking that model probabilistically.

## Features

- **Zero dependencies** — uses only the Python standard library (`collections`, `random`)
- **Sentence-aware tokenization** — lowercases and strips punctuation, tracking sentence boundaries
- **Weighted random generation** — picks the next word proportional to how often it followed the current word in the source text
- **Configurable** — choose a starting word and output length, or let the generator pick a starter automatically
- **O(n) chain construction** — the transition model is built in a single pass over the corpus

## Project Structure

```
.
├── chain.py       # Core Markov chain: build, store, and generate
├── tokenizer.py   # Text → list of sentences → list of words
└── main.py        # Demo: runs the generator on a sample paragraph
```

## How It Works

### 1. Tokenization (`tokenizer.py`)

`tokenize_text` splits raw text on whitespace, lowercases each token, and strips trailing punctuation. A sentence ends whenever a raw token finishes with `.`, `!`, or `?`.

```python
tokenize_text("The cat sat. The dog ran!")
# → [["the", "cat", "sat"], ["the", "dog", "ran"]]
```

### 2. Building the Chain (`chain.py`)

`build_chain` walks every sentence and, for each adjacent word pair, records a transition:

```python
chain[current][next_word] += 1
```

The result is a `defaultdict(Counter)` — a map from each word to a frequency count of the words that followed it.

`get_starters` collects a `Counter` of the first word of every sentence, which is used to pick a natural-looking starting point.

Both are bundled together by `get_data` into an immutable `ChainData` namedtuple:

```python
ChainData(sentences=..., starts=..., chain=...)
```

### 3. Generation (`chain.py`)

`generate` picks a starting word (either supplied or drawn from `starts`, weighted by frequency) and then repeatedly asks the chain "what usually comes next?" via `weighted_pick`, which uses `random.choices` to sample proportionally to the recorded counts.

Generation stops early if it reaches a word with no recorded followers (a dead end).

## Usage

### Run the demo

```bash
python main.py
```

This tokenizes the sample paragraph embedded in `main.py`, prints some statistics about the learned model, then generates ten random passages of 50 words each.

### Use it in your own code

```python
from tokenizer import tokenize_text
from chain import get_data, generate

text = open("corpus.txt").read()
data = get_data(tokenize_text(text))

# Let the generator choose a starting word
print(" ".join(generate(data, length=40)))

# Or force a specific start
print(" ".join(generate(data, start="the", length=40)))
```

## API Reference

| Function | Description |
|---|---|
| `tokenize_text(text) -> list[list[str]]` | Split text into sentences of cleaned words. |
| `get_starters(sentences) -> Counter[str]` | Count how often each word begins a sentence. |
| `build_chain(sentences) -> defaultdict[str, Counter]` | Build the word → follower-counts transition map. |
| `get_data(sentences) -> ChainData` | Bundle sentences, starters, and chain into one object. |
| `weighted_pick(counter) -> str` | Pick a key from a `Counter`, weighted by its count. |
| `generate(data, start=None, length=20) -> list[str]` | Generate a list of `length` words from the chain. |

## Notes & Limitations

- **Order-1 chain.** Only the immediately preceding word influences the next one. This produces locally plausible but globally loose text. For more coherence, extend the key to n-grams (e.g. tuples of two or three words).
- **No smoothing.** If a word never appeared in the source text, the generator can't produce it, and generation halts at any word with no recorded successors.
- **Case and punctuation are lost.** All output is lowercase and unpunctuated. Reconstructing sentence casing and punctuation is left as an exercise.
- **Reproducibility.** Results vary between runs. Seed `random` if you want deterministic output:

  ```python
  import random
  random.seed(42)
  ```

## License

Public domain / MIT — do whatever you like with it.