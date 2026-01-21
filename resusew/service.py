import json
from bs4 import BeautifulSoup

def run(resume: str, keywords: str, jobdesc: str) -> str:
    soup: BeautifulSoup = BeautifulSoup(resume, "html.parser")
    kw: dict = json.loads(keywords)

    templates = soup.find_all(**{ "class": "resusew" })
    for t in templates:
        print(t.get("id"))

    return ""

