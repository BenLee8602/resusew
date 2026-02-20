import pytest
from resusew import TokenTrie


def test_trie():
    trie: TokenTrie = TokenTrie()

    assert trie.insert(["c"])
    assert trie.insert(["c", "+", "+"])
    assert trie.insert(["c", "#"])

    assert trie.insert(["react"])
    assert trie.insert(["react", "native"])

    assert trie.insert(["asp", "net"])
    assert trie.insert(["asp", "net", "core"])

    assert trie.insert(["net"])
    assert not trie.insert(["net"])

    assert trie.search(["c"])
    assert trie.search(["c", "+", "+"])
    assert trie.search(["c", "#"])

    assert trie.search(["react"])
    assert trie.search(["react", "native"])

    assert trie.search(["net"])
    assert trie.search(["asp", "net"])
    assert trie.search(["asp", "net", "core"])

    assert not trie.search(["asp"])
    assert trie.search_prefix(["asp"])
    assert trie.search_prefix(["c"])

    assert trie.delete(["react"])
    assert not trie.delete(["react"])
    assert not trie.search(["react"])
    assert trie.search_prefix(["react"])
    assert trie.search(["react", "native"])

