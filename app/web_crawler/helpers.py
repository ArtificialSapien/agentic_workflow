from bs4 import BeautifulSoup
from app.web_crawler.data_model import NewsArticle

import datetime
import httpx
import pathlib
import requests


def extract_text_from_website(url: str) -> str:
    """
    Extract content from a website that can be accessed via a provided URL.
    Will try to follow redirects.

    :url: URL of the website (html file)
    :exception: Might throw exceptions e.g. HTTPStatusError

    :return: Extracted content
    """
    r = requests.head(url, allow_redirects=True)

    final_url = r.url
    if not final_url == url:
        print(f"URL redirected\n  FROM: {url}\n  TO: {final_url}")

    html_response = httpx.get(final_url)
    html_response.raise_for_status()
    page = html_response.text
    soup = BeautifulSoup(page, 'html.parser')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return str(text.encode('utf-8'))


def create_article_summaries_from_metadata_file(source: str = "arxiv"):
    if not pathlib.Path(f"work/{source}").exists():
        raise ValueError(f"Directory for news source '{source}' does not exist")
    meta_data_file_path = f"work/{source}/metadata.txt"
    if not pathlib.Path(f"work/{source}/metadata.txt").exists():
        raise ValueError(f"metadata.txt does not exist for news source '{source}'")

    with open(meta_data_file_path, "r") as fl:
        for line in fl:
            fields = line.split('|')
            article_id = fields[0]
            article_summary_path = f"work/{source}/summaries/{article_id}.txt"
            summary = ""
            with open(article_summary_path, "r") as summary_file:
                summary = summary_file.read()
            news_article = NewsArticle(
                title=str(fields[3]),
                date=str(datetime.date.today()),
                content=str(summary),
                author=str(fields[1]),
                source=str(fields[2])
            )

            with open(f"work/{source}/output/{article_id}.json", 'w') as outfile:
                outfile.write(news_article.model_dump_json(indent=2))


class Timer:
    def __init__(self, print: bool = True):
        self.__print = print
        self.__start_time = None
        self.__stop_time = None

    def tic(self):
        self.__start_time = datetime.now()

    def toc(self, note: str = "") -> float:
        self.__stop_time = datetime.now()
        elapsed_time = self.__stop_time - self.__start_time
        if self.__print:
            if note:
                note = f" ({note})"
            print(f"Elapsed time{note}: {elapsed_time}s")
        return elapsed_time
