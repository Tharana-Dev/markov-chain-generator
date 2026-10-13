# tests/test_chain.py

from collections import Counter

import pytest

from chain import collect_words, find_path, shortest_path


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