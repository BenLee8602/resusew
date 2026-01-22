import sys
import resusew

def load_required_file(filename: str) -> str:
    try:
        with open(filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        exit(1)

if len(sys.argv) != 5:
    print(
        "usage: py -m resusew "
        "resume.html "
        "keywords.json "
        "jobdesc.txt "
        "out.html"
    )
    exit(1)

resume_file: str = sys.argv[1]
keywords_file: str = sys.argv[2]
jobdesc_file: str = sys.argv[3]
out_file: str = sys.argv[4]

resume: str = load_required_file(resume_file)
keywords: str = load_required_file(keywords_file)
jobdesc: str = load_required_file(jobdesc_file)

out: str = resusew.run(resume, keywords, jobdesc)

try:
    with open(out_file, 'w') as f:
        f.write(out)
except Exception as e:
    print(e)
    exit(1)

