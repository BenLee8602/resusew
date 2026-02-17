import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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

    def __init__(self, jobdesc: str):
        self.jobdesc: list[str] = self.__tokenize(jobdesc)
        self.kw_cache: dict[str, int] = {}
        self.itemkw_stack: list[set[str]] = []


    def push(self, itemkw: set[str]) -> None:
        self.itemkw_stack.append(itemkw)

    def pop(self) -> set[str]:
        return self.itemkw_stack.pop()

    def update(self, kws: set[str]) -> None:
        self.itemkw_stack[-1].update(kws)


    def get_kw_score(self, kw: str) -> int:
        if len(kw) == 0:
            return 0

        if kw in self.kw_cache:
            return self.kw_cache[kw]
        kwt: list[str] = self.__tokenize(kw)

        count: int = 0
        i: int = 0
        while i <= len(self.jobdesc) - len(kwt):
            for j in range(len(kwt)):
                if kwt[j] != self.jobdesc[i + j]:
                    i += 1
                    break
                if j == len(kwt) - 1:
                    i += len(kwt)
                    count += 1
        
        self.kw_cache[kw] = count
        return count


    def __tokenize(self, s: str) -> list[str]:
        s = s.lower()
        tokens: list[str] = wordpunct_tokenize(s)
        tokens = [t for t in tokens if t not in Job.__BAD_TOKENS]
        tokens = [Job.__LEMMATIZER.lemmatize(t) for t in tokens]
        return tokens

