from resusew import Job, Resusew

class StaticText(Resusew):
    def __init__(self, text: list[str]):
        self.text = text

    def resolve(self, job: Job) -> None:
        pass

    def to_plain_str(self) -> list[str]:
        return self.text

    def to_template_str(self) -> list[str]:
        return self.text

