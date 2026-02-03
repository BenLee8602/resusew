import pytest
import resusew


def load_test_data(filename: str) -> str:
    DATA_PATH = "tests/data/"
    try:
        with open(DATA_PATH + filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        assert False


def test_service():
    resume: str = load_test_data("resume.txt.resusew")

    for i in range(3):
        job: str = load_test_data(f"job{i + 1}.txt")
        expected: str = load_test_data(f"resume{i + 1}.txt")
        actual = resusew.run(resume, job)
        assert expected == actual

