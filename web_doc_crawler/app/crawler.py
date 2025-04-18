import os
import requests
from bs4 import BeautifulSoup
import html2text

DOCS = {
    "langchain": "https://docs.langchain.com/docs/",
    "langgraph": "https://docs.langgraph.dev/",
    "pydantic": "https://docs.pydantic.dev/latest/"
}

def save_markdown(framework, title, html):
    from pathlib import Path
    output_dir = Path("docs") / framework
    output_dir.mkdir(parents=True, exist_ok=True)

    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    markdown = text_maker.handle(html)
    filename = title.replace("/", "_") + ".md"
    with open(output_dir / filename, "w", encoding="utf-8") as f:
        f.write(markdown)

def crawl_and_convert(framework, url, visited=set()):
    if url in visited or not url.startswith(DOCS[framework]):
        return
    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        save_markdown(framework, url.replace(DOCS[framework], "").strip("/") or "index", str(soup))

        for link in soup.find_all("a"):
            href = link.get("href", "")
            if href.startswith("/") or href.startswith(DOCS[framework]):
                next_url = href if href.startswith("http") else DOCS[framework] + href.lstrip("/")
                crawl_and_convert(framework, next_url, visited)
    except:
        pass

def crawl_docs(framework):
    if framework not in DOCS:
        return
    crawl_and_convert(framework, DOCS[framework], set())