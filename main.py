from tokenizer import tokenize_text
from chain import (
    get_data,
    generate,
    generate_stream,
    collect_words,
    find_path,
    shortest_path_cached,
)
import random
from datetime import datetime
from itertools import islice
import time


def get_random_sample(filename: str, num_paragraphs: int = 50) -> str:
    """
    Open a file, split it into paragraphs, randomly sample a number of them,
    and join the sample back together with blank lines.
    """
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    sample_size = min(len(paragraphs), num_paragraphs)
    sampled_paragraphs = random.sample(paragraphs, sample_size)

    return "\n\n".join(sampled_paragraphs)


if __name__ == "__main__":
    RULE = "─" * 64

    # ── 1. Load the sample text ──────────────────────────────────────────
    SAMPLE = get_random_sample("sample_text.txt", 50)
    sentences = tokenize_text(SAMPLE)

    # REQUIREMENT 1: build the chain with pairwise transitions
    data = get_data(sentences)

    # ── 2. Start the output buffer ───────────────────────────────────────
    output_lines = [
        RULE,
        " SAMPLE SUMMARY",
        RULE,
        f" Text length   : {len(SAMPLE):,} characters",
        f" Starters      : {data.starts.most_common(5)}",
        f" After 'the'   : {data.chain['the'].most_common(5)}",
        "",
        RULE,
        " GENERATED TEXTS",
        RULE,
    ]

    # ── 3. Ten generated samples ─────────────────────────────────────────
    for i in range(1, 11):
        output_lines.append(f" {i:>2}. " + " ".join(generate(data, length=25)))
    output_lines.append("")

    # ── 4. Pick a reachable start/target pair ────────────────────────────
    all_words = [w for w in data.chain.keys() if data.chain[w]]
    start_word, target_word = None, None

    if all_words:
        random.shuffle(all_words)
        for candidate in all_words:
            reachable = collect_words(data.chain, candidate)
            choices = list(reachable - {candidate})
            if choices:
                start_word = candidate
                target_word = random.choice(choices)
                break

    if not start_word or not target_word:
        if len(all_words) >= 2:
            start_word, target_word = all_words[0], all_words[1]
        else:
            start_word, target_word = "unknown", "unknown"

    dfs_route = find_path(data.chain, start_word, target_word)

    # REQUIREMENT 2: shortest_path_cached, timed twice (miss, then hit)
    t1_start = time.perf_counter()
    bfs_route_first = shortest_path_cached(data.chain, start_word, target_word)
    t1_end = time.perf_counter()

    t2_start = time.perf_counter()
    bfs_route_second = shortest_path_cached(data.chain, start_word, target_word)
    t2_end = time.perf_counter()

    first_duration = t1_end - t1_start
    second_duration = t2_end - t2_start
    speed_gain = first_duration / second_duration if second_duration > 0 else float("inf")

    speed_label = (
        f"{speed_gain:.2f}x faster"
        if speed_gain != float("inf")
        else "instantaneous (0.0s)"
    )

    # ── 5. Graph traversal report ────────────────────────────────────────
    output_lines.extend([
        RULE,
        " GRAPH TRAVERSAL",
        RULE,
        f" Reachable from 'the'    : {sorted(collect_words(data.chain, 'the'))}",
        "",
        f" Start word              : '{start_word}'",
        f" Target word             : '{target_word}'",
        "",
        f" DFS route               : {dfs_route}",
        "",
        f" BFS route 1 (calculated): {bfs_route_first}",
        f"   └─ duration           : {first_duration:.8f} s",
        f" BFS route 2 (cached hit): {bfs_route_second}",
        f"   └─ duration           : {second_duration:.8f} s",
        f"   └─ performance        : second call was {speed_label}",
        "",
    ])

    # ── 6. Lazy generator demo ───────────────────────────────────────────
    # REQUIREMENT 3: islice pulls the first 10 words, no manual break needed
    output_lines.extend([
        RULE,
        " LAZY GENERATOR STREAM",
        RULE,
        " First 10 words of a 10,000-word stream:",
    ])
    for word in islice(generate_stream(data, length=10_000), 10):
        output_lines.append(f"   • {word}")
    output_lines.append("")

    # ── 7. Console output + append to the runtime log ────────────────────
    full_output = "\n".join(output_lines)
    print(full_output)

    with open("output.txt", "a", encoding="utf-8") as out_file:
        out_file.write(f"\n\n{RULE}\n")
        out_file.write(f" RUNTIME LOG · {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_file.write(f"{RULE}\n")
        out_file.write(full_output)

    print("\n[SUCCESS] Entry successfully appended to 'output.txt'!")