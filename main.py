from tokenizer import tokenize_text
from chain import get_data, generate_stream, generate, shortest_path, find_path, collect_words
import random
from datetime import datetime

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
    bfs_route = shortest_path(data.chain, start_word, target_word)

    # 5. Add graph traversal metrics straight into the buffer
    output_lines.extend([
        "--- Graph Traversal Demos ---",
        f"Reachable from 'the': {sorted(collect_words(data.chain, 'the'))}\n",
        f"DFS path from '{start_word}' to '{target_word}': {dfs_route}\n",
        f"BFS path from '{start_word}' to '{target_word}': {bfs_route}\n",
        "--- Generator Demo (Lazy Stream) ---",
        "First 5 words from an infinite-ish generator:"
    ])

    for i, word in enumerate(generate_stream(data, length=10_000)):
        if i >= 5:
            break
        output_lines.append(f"  {word}")

    # 6. --- THE DUAL CONSOLE & APPEND LOG SYSTEM ---
    full_output = "\n".join(output_lines)
    
    # Action 1: Print directly to your terminal screen as usual
    print(full_output)
    
    # Action 2: APPEND straight to your historical log file
    with open("output.txt", "a", encoding="utf-8") as out_file:
        # Create a clear visual separator with a real-time stamp for each run
        out_file.write(f"\n\n{'='*50}\n")
        out_file.write(f" RUNTIME LOG: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_file.write(f"{'='*50}\n")
        
        # Append the new generated text
        out_file.write(full_output)
        
    print("\n[SUCCESS] Entry successfully appended to 'output.txt'!")