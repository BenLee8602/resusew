import sys
import resusew.service

def load_required_file(filename: str) -> str:
    try:
        with open(filename) as f:
            return f.read()
    except Exception as e:
        print(e)
        exit(1)

if len(sys.argv) != 4:
    print("usage: py -m resusew resume.html keywords.json jobdesc.txt")
    exit(1)

resume_file: str = sys.argv[1]
keywords_file: str = sys.argv[2]
jobdesc_file: str = sys.argv[3]

resume: str = load_required_file(resume_file)
keywords: str = load_required_file(keywords_file)
jobdesc: str = load_required_file(jobdesc_file)

resusew.service.run(resume, keywords, jobdesc)

