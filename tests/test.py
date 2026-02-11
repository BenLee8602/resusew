import pytest
from copy import deepcopy
from resusew import Parser, Job, Resusew


def load_test_data(filename: str) -> str:
    DATA_PATH = "tests/data/"
    try:
        with open(DATA_PATH + filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        assert False


def test_all():
    parser: Parser = Parser()
    resume_text: list[str] = load_test_data("resume.txt.resusew").split('\n')
    resume: Resusew = parser.parse(resume_text)

    for i in range(3):
        resume_cur: Resusew = deepcopy(resume)

        job_text: str = load_test_data(f"job{i + 1}.txt")
        job: Job = Job(job_text)

        resume_cur.resolve(job)

        expected: str = load_test_data(f"resume{i + 1}.txt")
        actual = '\n'.join(resume_cur.to_plain_str())
        assert expected == actual

