class TokenTrie:
    def __init__(self):
        self.kids: dict[str, TokenTrie] = {}
        self.end: bool = False


    def nav(self, tokens: list[str]) -> list:
        nodes: list[TokenTrie] = [self]
        for t in tokens:
            if t not in nodes[-1].kids:
                break
            nodes.append(nodes[-1].kids[t])
        return nodes


    def insert(self, tokens: list[str]) -> bool:
        nodes: list[TokenTrie] = self.nav(tokens)
        for t in tokens[len(nodes) - 1:]:
            nodes[-1].kids[t] = TokenTrie()
            nodes.append(nodes[-1].kids[t])
        exists: bool = nodes[-1].end is True
        nodes[-1].end = True
        return not exists


    def delete(self, tokens: list[str]) -> bool:
        nodes: list[TokenTrie] = self.nav(tokens)
        if len(nodes) - 1 != len(tokens) or not nodes[-1].end:
            return False
        nodes[-1].end = False
        while tokens:
            if nodes[-1].end or nodes[-1].kids:
                break
            nodes.pop()
            nodes[-1].kids.pop(tokens[-1])
            tokens.pop()
        return True


    def search(self, tokens: list[str]) -> bool:
        nodes: list[TokenTrie] = self.nav(tokens)
        return len(nodes) - 1 == len(tokens) and nodes[-1].end

    def search_prefix(self, tokens: list[str]) -> bool:
        nodes: list[TokenTrie] = self.nav(tokens)
        return len(nodes) - 1 == len(tokens)

