import json
import os
from importlib import resources
from argparse import ArgumentParser
from resusew import Parser, Job, Resusew


def _load_args():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "resume",
        help="your resusew template file")
    parser.add_argument(
        "jobdesc",
        help="job description file")
    parser.add_argument(
        "out",
        help="tailored resume output file")
    parser.add_argument(
        "-a",
        "--alias",
        help="your keyword alias dict file")
    return parser.parse_args()


def _load_required_file(filename: str) -> str:
    try:
        with open(filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        exit(1)


def _load_static_file(filename: str) -> str:
    static_dir: str = resources.files("resusew").joinpath("static")
    return static_dir.joinpath(filename).read_text()


def _load_alias(name: str | None) -> dict[str, list[str]]:
    if name is None:
        return {}

    alias_presets: set[str] = {"swe"}
    if name not in alias_presets:
        return json.loads(_load_required_file(name))

    return json.loads(_load_static_file(os.path.join(
        "alias", name + ".json")))


def main():
    args = _load_args()

    resume_str: str = _load_required_file(args.resume)
    jobdesc_str: str = _load_required_file(args.jobdesc)
    alias: dict[str, list[str]] = _load_alias(args.alias)

    resume: Resusew = Parser().parse(resume_str.split('\n'))
    jobdesc: Job = Job(jobdesc_str, resume.get_keywords(), alias)

    resume.resolve(jobdesc)
    out = '\n'.join(resume.to_plain_str())

    try:
        with open(args.out, 'w') as f:
            f.write(out)
    except Exception as e:
        print(e)
        exit(1)

