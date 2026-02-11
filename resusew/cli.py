import sys
from resusew import Parser, Job, Resusew

def load_required_file(filename: str) -> str:
    try:
        with open(filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        exit(1)

def main():
    if len(sys.argv) != 4:
        print(
            "usage: resusew "
            "resume.xyz.resusew "
            "jobdesc.txt "
            "out.xyz"
        )
        exit(1)

    resume_file: str = sys.argv[1]
    jobdesc_file: str = sys.argv[2]
    out_file: str = sys.argv[3]

    resume_str: str = load_required_file(resume_file)
    jobdesc_str: str = load_required_file(jobdesc_file)

    resume: Resusew = Parser().parse(resume_str.split('\n'))
    jobdesc: Job = Job(jobdesc_str)

    resume.resolve(jobdesc)
    out = '\n'.join(resume.to_plain_str())

    try:
        with open(out_file, 'w') as f:
            f.write(out)
    except Exception as e:
        print(e)
        exit(1)

