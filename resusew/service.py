import json
from nltk.tokenize import wordpunct_tokenize


_CMD_ITEM = "__RESUSEW_ITEM__"
_CMD_BEG = "__RESUSEW_BEG__"
_CMD_END = "__RESUSEW_END__"


class _State:
    resume: list[str] = []
    itemkw_stack: list[set[str]] = []
    jobdesc: tuple[str] = ()
    kw_cache: dict[str, int] = {}

class _Item:
    def __init__(self):
        self.keywords: set(str) = set()
        self.content: list[str] = []
        self.score: int = 0


def _peek_word() -> str:
    i: int = _State.resume[0].find(' ')
    if i == -1:
        return _State.resume[0]
    return _State.resume[0][:i]

def _pop_word() -> str:
    i: int = _State.resume[0].find(' ')
    if i == -1:
        return _State.resume[0]
    word: str = _State.resume[0][:i]
    _State.resume[0] = _State.resume[0][i + 1:]
    return word

def _pop_line() -> str:
    return _State.resume.pop(0)


def _tokenize(s: str) -> tuple[str]:
    return tuple(wordpunct_tokenize(s.lower()))

def _get_kw_score(kw: str) -> int:
    if len(kw) == 0:
        return 0

    if kw in _State.kw_cache:
        return _State.kw_cache[kw]
    kwt: tuple[str] = _tokenize(kw)

    count: int = 0
    i: int = 0
    while i <= len(_State.jobdesc) - len(kwt):
        for j in range(len(kwt)):
            if kwt[j] != _State.jobdesc[i + j]:
                i += 1
                break
            if j == len(kwt) - 1:
                i += len(kwt)
                count += 1
    
    _State.kw_cache[kw] = count
    return count


def _parse_template() -> list[str]:
    items: list[_Item] = []
    max_items: int = 0

    while _State.resume:
        cmd: str = _pop_word()
        if cmd == _CMD_END:
            max_items = int(_pop_line())
            break
        items.append(_parse_item())

    items.sort(reverse=True, key=lambda i: i.score)

    content: list[str] = []
    for item in items[:min(max_items, len(items))]:
        content += item.content
        _State.itemkw_stack[-1].update(item.keywords)
    return content


def _parse_item() -> _Item:
    item: _Item = _Item()
    _State.itemkw_stack.append(item.keywords)
    
    keywords: str = _pop_line()
    if keywords:
        item.keywords = set(keywords.split(','))

    while _State.resume:
        cmd: str = _peek_word()
        if cmd == _CMD_ITEM or cmd == _CMD_END:
            break
        if cmd == _CMD_BEG:
            item.content += _parse_template()
        else:
            item.content.append(_pop_line())

    _State.itemkw_stack.pop()
    for kw in item.keywords:
        item.score += _get_kw_score(kw)

    return item


def run(resume: str, jobdesc: str) -> str:
    _State.resume = [""] + resume.split('\n')
    _State.itemkw_stack = []
    _State.jobdesc = _tokenize(jobdesc)
    _State.kw_cache = {}

    return '\n'.join(_parse_item().content)


__all__ = ["run"]

