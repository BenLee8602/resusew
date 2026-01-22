import json
from bs4 import BeautifulSoup, Tag, NavigableString


_target: str = ""
_kw_cache: dict[str, int] = {}


def _is_whitespace_node(node: Tag | NavigableString) -> bool:
    return isinstance(node, NavigableString) and node.strip() == ""


def _get_node_score(keywords: list[str]) -> int:
    global _kw_cache
    score: int = 0

    for kw in keywords:
        kw = kw.lower()
        if kw in _kw_cache:
            score += _kw_cache[kw]
            continue

        s: int = _target.count(kw)
        _kw_cache[kw] = s
        score += s

    return score


def run(resume: str, keywords: str, jobdesc: str) -> str:
    global _target, _kw_cache

    soup: BeautifulSoup = BeautifulSoup(resume, "html.parser")
    keywords: dict = json.loads(keywords)
    _target = jobdesc.lower()
    _kw_cache = {}

    templates = soup.find_all(**{ "class": "resusew" })
    for t in templates:
        nodes: list[Tag] = list(filter(
            lambda n: not _is_whitespace_node(n),
            t.children
        ))
        kw: list[str] = keywords[t["id"]]

        for i, n in enumerate(nodes):
            n["data-resusew-score"] = _get_node_score(kw[i])
        nodes.sort(reverse=True, key=lambda n : n["data-resusew-score"])

        sel_count: int = int(t["data-resusew-count"])
        for i in range(min(sel_count, len(nodes))):
            t.insert_before(nodes[i])

        t.decompose()

    return soup.prettify()


__all__ = ["run"]

