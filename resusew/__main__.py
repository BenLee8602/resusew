import sys
import resusew

def load_required_file(filename: str) -> str:
    try:
        with open(filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        exit(1)

if len(sys.argv) != 4:
    print(
        "usage: py -m resusew "
        "resume.xyz.resusew "
        "jobdesc.txt "
        "out.xyz"
    )
    exit(1)

resume_file: str = sys.argv[1]
jobdesc_file: str = sys.argv[2]
out_file: str = sys.argv[3]

resume: str = load_required_file(resume_file)
jobdesc: str = load_required_file(jobdesc_file)

out: str = resusew.run(resume, jobdesc)

try:
    with open(out_file, 'w') as f:
        f.write(out)
except Exception as e:
    print(e)
    exit(1)

