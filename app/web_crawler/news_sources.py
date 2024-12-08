import hashlib
import json
import pathlib
from abc import ABC, abstractmethod
from typing import List, Dict

import os

from httpx import HTTPStatusError

from app.web_crawler.data_model import NewsArticle
from app.web_crawler.domain import NewsProvider
from serpapi import GoogleSearch

from app.web_crawler.helpers import extract_text_from_website


class NewsSource(ABC):
    @abstractmethod
    def fetch(self, search_parameters: dict) -> None:
        pass

    @abstractmethod
    def store_raw_data(self, filename: str) -> None:
        pass

    @abstractmethod
    def get_news_content(self, limit: int = 1):
        pass


class GoogleNewsSource(NewsSource):
    def __init__(self):
        self.__SERP_API_KEY = os.getenv("SERP_API_KEY")
        assert self.__SERP_API_KEY is not None
        self.__last_result = ""
        self.__source = NewsProvider.GOOGLE

    def fetch(self, search_parameters: dict = {"q": "artificial intelligence"}) -> None:
        GoogleSearch.SERP_API_KEY = self.__SERP_API_KEY
        search = GoogleSearch(search_parameters)
        self.__last_result = search.get_dict()
        with open("google_fetch.json", "w") as f:
            f.write(json.dumps(self.__last_result, indent=2))

    def store_raw_data(self, filename: str) -> None:
        source = NewsProvider.GOOGLE
        filepath = f"work/{source}/{filename}.json"
        with open(filepath, "w") as file:
            file.write(str(self.__last_result))

    def get_news_content(self, limit: int = 1) -> List[NewsArticle]:
        news_articles = []
        news_results = self.__last_result["news_results"][:limit]
        for i_news, news_result in enumerate(news_results):
            print(f"""News p: {i_news + 1}/{len(news_results)}""")

            if "stories" in news_result:
                for i_story, story in enumerate(news_result["stories"]):
                    print(f"""  Story: {i_story + 1}/{len(news_result["stories"])}""")

                    news_article_content = self.process(story)
                    if news_article_content is not None:
                        authors = ""
                        if "authors" in story["source"]:
                            authors = '|'.join(story["source"]["authors"])
                        news_article = NewsArticle(
                            title=str(story["title"]),
                            date=str(story["date"]),
                            content=str(news_article_content),
                            author=str(authors),
                            source=str(story["link"])
                        )
                        news_articles.append(news_article)
            else:
                story = news_result

                news_article_content = self.process(story)
                if news_article_content is not None:
                    authors = ""
                    if "authors" in story["source"]:
                        authors = '|'.join(story["source"]["authors"])
                    news_article = NewsArticle(
                        title=str(story["title"]),
                        date=str(story["date"]),
                        content=str(news_article_content),
                        author=str(authors),
                        source=str(story["link"])
                    )
                    news_articles.append(news_article)

        return news_articles

    def process(self, story) -> dict:
        try:
            article_id = hashlib.md5(string=story["link"].encode("utf-8")).hexdigest()
            content = extract_text_from_website(story["link"])
            return {
                "article_id": article_id,
                "content": content
            }
        except HTTPStatusError as e:
            print(f"Ignoring this story, problem with the content fetching: {e}")
        except BaseException as e:
            print(f"Ignoring this story, an unknown problem occurred: {e}")
