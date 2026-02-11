from resusew import macro, StaticText, Item, Template

class Parser:
    def __init__(self):
        self.text: list[str] = []

    def parse(self, text: list[str]) -> Item:
        self.text = [""] + text
        item: Item = self.__parse_item()
        self.text = []
        return item


    def __peek_word(self) -> str:
        i: int = self.text[0].find(' ')
        if i == -1:
            return self.text[0]
        return self.text[0][:i]

    def __pop_word(self) -> str:
        line: str = self.text[0]
        i: int = line.find(' ')
        if i == -1:
            self.text[0] = ""
            return line
        word: str = line[:i]
        self.text[0] = line[i + 1:]
        return word

    def __pop_line(self) -> str:
        return self.text.pop(0)


    def __parse_static_text(self) -> StaticText:
        text: list[str] = []
        while self.text:
            if self.__peek_word() in macro.ALL:
                break
            text.append(self.__pop_line())
        return StaticText(text)


    def __parse_item(self) -> Item:
        kw_str: str = self.__pop_line()

        keywords: set[str] = set(kw_str.split(',')) if kw_str else set()
        content: list[StaticText | Template] = []

        current: list[str] = []
        while self.text:
            word: str = self.__peek_word()
            if word == macro.BEG:
                if current:
                    content.append(StaticText(current))
                current = []
                content.append(self.__parse_template())
            elif word in macro.ALL:
                break
            else:
                current.append(self.__pop_line())
        if current:
            content.append(StaticText(current))

        return Item(keywords, content)


    def __parse_template(self) -> Template:
        items: list[Item] = []
        while self.text:
            word: str = self.__pop_word()
            if word == macro.END:
                break
            items.append(self.__parse_item())
        max_items: int = int(self.__pop_line())
        return Template(items, max_items)

