# tests/test_chain.py

from collections import Counter
import random
from chain import get_data, collect_words, find_path, shortest_path, generate, generate_stream


class TestCollectWords:
    def test_simple_chain(self):
        chain = {
            "a": {"b", "c"},
            "b": {"d"},
            "c": {"d", "e"},
            "d": set(),
            "e": set(),
        }
        assert collect_words(chain, "a") == {"a", "b", "c", "d", "e"}

    def test_cycle(self):
        chain = {"a": {"b"}, "b": {"c"}, "c": {"a"}}
        assert collect_words(chain, "a") == {"a", "b", "c"}

    def test_word_not_in_chain(self):
        assert collect_words({}, "x") == {"x"}

    def test_leaf_word(self):
        chain = {"a": []}
        assert collect_words(chain, "a") == {"a"}


class TestFindPath:
    def test_simple_path(self):
        chain = {"a": ["b"], "b": ["c"], "c": ["d"]}
        assert find_path(chain, "a", "d") == ["a", "b", "c", "d"]

    def test_start_equals_target(self):
        assert find_path({}, "a", "a") == ["a"]

    def test_no_path(self):
        chain = {"a": ["b"], "b": []}
        assert find_path(chain, "a", "z") is None

    def test_start_not_in_chain(self):
        assert find_path({}, "a", "b") is None

    def test_cycle_with_no_target(self):
        chain = {"a": ["b"], "b": ["a"]}
        assert find_path(chain, "a", "c") is None

    def test_multiple_branches(self):
        chain = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
        # DFS explores "b" first because it is first in the list
        assert find_path(chain, "a", "d") == ["a", "b", "d"]


class TestShortestPath:
    def test_simple_path(self):
        graph = {"a": {"b": 1}, "b": {"c": 1}, "c": {"d": 1}, "d": {}}
        assert shortest_path(graph, "a", "d") == ["a", "b", "c", "d"]

    def test_start_equals_target(self):
        assert shortest_path({}, "a", "a") == ["a"]

    def test_no_path(self):
        graph = {"a": {"b": 1}, "b": {}}
        assert shortest_path(graph, "a", "z") is None

    def test_unreachable_cycle(self):
        graph = {"a": {"b": 1}, "b": {"a": 1}}
        assert shortest_path(graph, "a", "z") is None

    def test_shortest_of_multiple_paths(self):
        graph = {
            "a": {"b": 1, "c": 1},
            "b": {"d": 1},
            "c": {"d": 1},
            "d": {"e": 1},
            "e": {},
        }
        path = shortest_path(graph, "a", "e")

        assert path is not None
        assert path[0] == "a"
        assert path[-1] == "e"
        assert len(path) == 4  # a -> b/c -> d -> e
        assert path in (
            ["a", "b", "d", "e"],
            ["a", "c", "d", "e"],
        )

    def test_with_counter_values(self):
        graph = {
            "a": Counter(["b"]),
            "b": Counter(["c"]),
            "c": Counter(),
        }
        assert shortest_path(graph, "a", "c") == ["a", "b", "c"]

    def test_start_not_in_graph(self):
        assert shortest_path({}, "x", "y") is None


import random

class TestGenerateStream:
    def test_matches_generate(self):
        sentences = [["the", "cat", "sat"], ["the", "dog", "ran"]]
        data = get_data(sentences)

        random.seed(42)
        list_version = generate(data, "the", 5)

        random.seed(42)                     # reset — same picks
        gen_version = list(generate_stream(data, "the", 5))

        assert list_version == gen_version

    def test_exhausts_after_one_pass(self):
        sentences = [["the", "cat", "sat"]]
        data = get_data(sentences)

        gen = generate_stream(data, "the", 3)
        first_pass = list(gen)
        second_pass = list(gen)

        assert len(first_pass) == 3
        assert second_pass == []            # exhausted

    def test_empty_input(self):
        data = get_data([])
        assert list(generate_stream(data)) == []

    def test_zero_length(self):
        sentences = [["a", "b"]]
        data = get_data(sentences)
        assert list(generate_stream(data, length=0)) == []