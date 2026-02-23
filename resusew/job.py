import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from resusew import TokenTrie


def _dl_nltk_data(resource_path: str, resource_name: str):
    try:
        nltk.data.find(resource_path)
    except LookupError:
        nltk.download(resource_name)

_dl_nltk_data("corpora/stopwords", "stopwords")
_dl_nltk_data("corpora/wordnet.zip", "wordnet")


class Job:
    __PUNCT: set[str] = set(",:;-'./\\?!_|\"()[]{}")
    __STOPWORDS: set[str] = set(stopwords.words("english"))

    __BAD_TOKENS: set[str] = __PUNCT | __STOPWORDS
    __LEMMATIZER: WordNetLemmatizer = WordNetLemmatizer()


    def __init__(self,
                 jobdesc: str,
                 keywords: set[str],
                 aliases: dict[str, list[str]]):

        self.itemkw_stack: list[set[str]] = []
        self.scores: dict[tuple[str], int] = {}

        job: list[str] = self.__tokenize(jobdesc)

        keyword_trie: TokenTrie = TokenTrie()
        alias_map: dict[tuple[str], tuple[str]] = {}
        for key, val in aliases.items():
            kt: tuple[str] = tuple(self.__tokenize(key))
            for v in val:
                vt: list[str] = self.__tokenize(v)
                keyword_trie.insert(vt)
                alias_map[tuple(vt)] = kt
        for kw in keywords:
            keyword_trie.insert(self.__tokenize(kw))

        while job:
            nodes: list[TokenTrie] = keyword_trie.nav(job)[1:]
            while nodes and not nodes[-1].end:
                nodes.pop()
            if nodes:
                kw: tuple[str] = tuple(job[:len(nodes)])
                kw = alias_map.get(kw, kw)
                self.scores[kw] = self.scores.get(kw, 0) + 1
            del job[:max(1, len(nodes))]


    def push(self, itemkw: set[str]) -> None:
        self.itemkw_stack.append(itemkw)

    def pop(self) -> set[str]:
        return self.itemkw_stack.pop()

    def update(self, kws: set[str]) -> None:
        self.itemkw_stack[-1].update(kws)


    def get_kw_score(self, kw: str) -> int:
        return self.scores.get(tuple(self.__tokenize(kw)), 0)


    def __tokenize(self, s: str) -> list[str]:
        s = s.lower()
        tokens: list[str] = wordpunct_tokenize(s)
        tokens = [t for t in tokens if t not in Job.__BAD_TOKENS]
        tokens = [Job.__LEMMATIZER.lemmatize(t) for t in tokens]
        return tokens

