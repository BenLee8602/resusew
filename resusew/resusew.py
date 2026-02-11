from abc import ABC, abstractmethod
from resusew import Job

class Resusew(ABC):
    @abstractmethod
    def resolve(self, job: Job) -> None:
        pass

    @abstractmethod
    def to_plain_str(self) -> list[str]:
        pass

    @abstractmethod
    def to_template_str(self) -> list[str]:
        pass

