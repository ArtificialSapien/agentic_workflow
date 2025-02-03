from abc import ABC, abstractmethod
from typing import List, Dict
from serpapi import GoogleSearch
from tavily import TavilyClient
from app.agents.data_models import NewsArticles

from app.web_crawler.web_search import scrape_article


class SearchEngine(ABC):
    """Abstract class for search engine APIs."""

    def __init__(self, api_key: str, params: Dict = None):
        self.api_key = api_key
        self.params = params

    @abstractmethod
    def search(self, query: str) -> NewsArticles:
        """Search for the given query."""
        pass


class GoogleSearchEngine(SearchEngine):
    """
    A search engine API using SerpAPI.

    Args:
        api_key (str): The API key for SerpAPI.
        params (Dict): The parameters for the search engine.

    Examples:
        params = {
            "engine": "google",
            "google_domain": "google.com",
            "gl": "us",
            "hl": "en",
        }
    """

    def __init__(self, api_key: str, params: Dict = None):
        if params is None:
            params = {
                "engine": "google",
                "google_domain": "google.com",
                "gl": "us",
                "hl": "en",
            }
        super().__init__(api_key, params)

    def search(self, query: str) -> List[str]:
        """Search for the given query using SerpAPI."""
        self.params.update({"q": query, "api_key": self.api_key})
        search = GoogleSearch(self.params)
        results = search.get_dict()

        news_articles = []
        limit = 5
        print(results)
        for result in results["organic_results"][:limit]:
            print(result["link"])
            news_articles.append(scrape_article(result["link"]))

        return news_articles


class TavilySearchEngine(SearchEngine):
    """
    A search engine API using Tavily.

    Args:
        api_key (str): The API key for Tavily.
        params (Dict): The parameters for the search engine.

    Examples:
        params = {
            search_depth: "advanced",
            topic: "general",
            days: 3,
            time_range: None,
            max_results: 5,
            include_images: False,
            include_image_descriptions: False,
            include_answer: "advanced",
            include_raw_content : True,
            include_domains:None,
            exclude_domains:None
        }
    """

    def __init__(self, api_key: str, params: Dict = None):
        if params is None:
            params = {
                "search_depth": "advanced",
                "topic": "general",
                "days": 3,
                "time_range": None,
                "max_results": 5,
                "include_images": False,
                "include_image_descriptions": False,
                "include_answer": None,
                "include_raw_content": True,
                "include_domains": None,
                "exclude_domains": None,
            }
        super().__init__(api_key, params)

    def search(self, query: str) -> List[str]:
        """Search for the given query using Tavily."""
        tavily_client = TavilyClient(self.api_key)

        response = tavily_client.search(query=query)  # , **self.params)

        news_articles = []
        for result in response["results"]:
            news_articles.append(scrape_article(result["url"]))

        return news_articles
