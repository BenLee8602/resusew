from resusew import macro, Job, Resusew

class Template(Resusew):
    def __init__(self, items: list[Resusew], max_items: int):
        self.items = items
        self.max_items = max_items


    def resolve(self, job: Job) -> None:
        scores: list[int] = []
        for i in self.items:
            i.resolve(job)

            score: int = 0
            for kw in i.keywords:
                score += job.get_kw_score(kw)
            scores.append(score)
        
        self.items, _ = zip(*sorted(
            zip(self.items, scores),
            key=lambda pair: pair[1],
            reverse=True
        ))
        self.items = self.items[:min(
            self.max_items,
            len(self.items)
        )]

        for i in self.items:
            job.update(i.keywords)
        

    def to_plain_str(self) -> list[str]:
        res: list[str] = []
        for i in self.items:
            res += i.to_plain_str()
        return res

    def to_template_str(self) -> list[str]:
        if not self.items:
            return []
        res: list[str] = self.__item_str(macro.BEG, self.items[0])
        for i in self.items[1:]:
            res += self.__item_str(macro.ITEM, i)
        res.append(macro.END + ' ' + str(self.max_items))
        return res

    def __item_str(self, macro: str, item: Resusew) -> list[str]:
        res: list[str] = [macro + ' ' + ','.join(item.keywords)]
        return res + item.to_template_str()

