from tokenizer import tokenize_text
from chain import get_data, shortest_path_cached,  generate_stream, generate, shortest_path, find_path, collect_words
import random
from datetime import datetime
from itertools import islice
import time

def get_random_sample(filename: str, num_paragraphs: int = 50) -> str:
    """
    Opens a file, splits it into paragraphs, randomly samples a specific
    number of paragraphs, and joins them back together with newlines.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    sample_size = min(len(paragraphs), num_paragraphs)
    
    sampled_paragraphs = random.sample(paragraphs, sample_size)
    return '\n\n'.join(sampled_paragraphs)

if __name__ == "__main__":
    # 1. Load the dynamic file sample text payload inside the main block
    SAMPLE = get_random_sample('sample_text.txt', 50)
    
    sentences = tokenize_text(SAMPLE)
    
    # REQUIREMENT 1: Runs build_chain with pairwise (Transparent swap)
    data = get_data(sentences)

    # 2. Initialize our output string collector array
    output_lines = [
        f"Text length: {len(SAMPLE)}",
        f"Starters: {data.starts.most_common(5)}",
        f"After 'the': {data.chain['the'].most_common(5)}\n",
        "--- Generated Texts ---"
    ]

    # 3. Add generated texts to the buffer
    for _ in range(10):
        output_lines.append(" ".join(generate(data, length=25)) + "\n")

    # 4. Execute your optimized graph discovery scan
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
    
    # REQUIREMENT 2: Show shortest_path_cached executing twice with time difference
    # First Call: Cache Miss (Triggers the full BFS scan)
    t1_start = time.perf_counter()
    bfs_route_first = shortest_path_cached(data.chain, start_word, target_word)
    t1_end = time.perf_counter()
    
    # Second Call: Cache Hit (Instantly returns the result from memory)
    t2_start = time.perf_counter()
    bfs_route_second = shortest_path_cached(data.chain, start_word, target_word)
    t2_end = time.perf_counter()
    
    # Calculate the elapsed durations in seconds
    first_duration = t1_end - t1_start
    second_duration = t2_end - t2_start
    
    # Calculate the relative performance gap safely
    speed_gain = first_duration / second_duration if second_duration > 0 else float('inf')

    # 5. Add graph traversal metrics straight into the buffer
    output_lines.extend([
        "--- Graph Traversal Demos ---",
        f"Reachable from 'the': {sorted(collect_words(data.chain, 'the'))}\n",
        f"DFS path from '{start_word}' to '{target_word}': {dfs_route}\n",
        f"BFS path 1 (Calculated): {bfs_route_first}",
        f"  └─ Duration: {first_duration:.8f} seconds",
        f"BFS path 2 (Cached Hit): {bfs_route_second}",
        f"  └─ Duration: {second_duration:.8f} seconds",
        f"  └─ Performance: Second call was {f'{speed_gain:.2f}x faster' if speed_gain != float('inf') else 'instantaneous (0.0s)'}!\n",
        "--- Generator Demo (Lazy Stream) ---",
        "First 10 words from an infinite-ish generator:"
    ])

    # REQUIREMENT 3: Use islice to grab the first 10 words without a manual loop break
    for word in islice(generate_stream(data, length=10_000), 10):
        output_lines.append(f"  {word}")

    # 6. --- THE DUAL CONSOLE & APPEND LOG SYSTEM ---
    full_output = "\n".join(output_lines)
    
    # Action 1: Print directly to your terminal screen as usual
    print(full_output)
    
    # Action 2: APPEND straight to your historical log file (Including the performance logs!)
    with open("output.txt", "a", encoding="utf-8") as out_file:
        # Create a clear visual separator with a real-time stamp for each run
        out_file.write(f"\n\n{'='*50}\n")
        out_file.write(f" RUNTIME LOG: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_file.write(f"{'='*50}\n")
        
        # Append the new generated text block
        out_file.write(full_output)
        
    print("\n[SUCCESS] Entry successfully appended to 'output.txt'!")
