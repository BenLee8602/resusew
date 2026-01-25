import json
from bs4 import BeautifulSoup, Tag, NavigableString
from nltk.tokenize import wordpunct_tokenize


Tokens = tuple[str]

class _State:
    target: Tokens = ()
    kw_cache: dict[str, int] = {}


def _is_whitespace_node(node: Tag | NavigableString) -> bool:
    return isinstance(node, NavigableString) and node.strip() == ""


def tokenize(s: str) -> Tokens:
    return tuple(wordpunct_tokenize(s.lower()))


def _get_kw_score(kw: str) -> int:
    if kw in _State.kw_cache:
        return _State.kw_cache[kw]
    kwt: Tokens = tokenize(kw)

    count: int = 0
    i: int = 0
    while i <= len(_State.target) - len(kwt):
        for j in range(len(kwt)):
            if kwt[j] != _State.target[i + j]:
                i += 1
                break
            if j == len(kwt) - 1:
                i += len(kwt)
                count += 1
    
    _State.kw_cache[kw] = count
    return count


def _resolve_template(t: Tag, kws: list[list[str]]) -> None:
    nodes: list[Tag] = list(filter(
        lambda n: not _is_whitespace_node(n),
        t.children
    ))

    for i, n in enumerate(nodes):
        score: int = 0
        for kw in kws[i]:
            score += _get_kw_score(kw)
        n["data-resusew-score"] = score
    nodes.sort(reverse=True, key=lambda n : n["data-resusew-score"])

    sel_count: int = int(t["data-resusew-count"])
    for i in range(min(sel_count, len(nodes))):
        t.insert_before(nodes[i])

    t.decompose()


def run(resume: str, keywords: str, jobdesc: str) -> str:
    soup: BeautifulSoup = BeautifulSoup(resume, "html.parser")
    keywords: dict = json.loads(keywords)
    _State.target = tokenize(jobdesc.lower())
    _State.kw_cache = {}

    templates = soup.find_all(**{ "class": "resusew" })
    for t in templates:
        _resolve_template(t, keywords[t["id"]])

    return soup.prettify()


__all__ = ["run"]

