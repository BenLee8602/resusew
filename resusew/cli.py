import json
from argparse import ArgumentParser
from resusew import Parser, Job, Resusew

def _load_required_file(filename: str) -> str:
    try:
        with open(filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        exit(1)

def main():
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
    args = parser.parse_args()

    resume_str: str = _load_required_file(args.resume)
    jobdesc_str: str = _load_required_file(args.jobdesc)

    aliases: dict[str, list[str]] = json.loads(
            _load_required_file(args.alias)) if args.alias else {}

    resume: Resusew = Parser().parse(resume_str.split('\n'))
    jobdesc: Job = Job(jobdesc_str, resume.get_keywords(), aliases)

    resume.resolve(jobdesc)
    out = '\n'.join(resume.to_plain_str())

    try:
        with open(args.out, 'w') as f:
            f.write(out)
    except Exception as e:
        print(e)
        exit(1)

