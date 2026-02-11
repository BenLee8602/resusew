from resusew import Job, Resusew

class Item(Resusew):
    def __init__(self, keywords: set[str], content: list[Resusew]):
        self.keywords: set[str] = keywords
        self.content: list[Resusew] = content

    def resolve(self, job: Job) -> int:
        job.push(self.keywords)
        for c in self.content:
            c.resolve(job)
        job.pop()

    def to_plain_str(self) -> list[str]:
        res: list[str] = []
        for c in self.content:
            res += c.to_plain_str()
        return res

    def to_template_str(self) -> list[str]:
        res: list[str] = []
        for c in self.content:
            res += c.to_template_str()
        return res

