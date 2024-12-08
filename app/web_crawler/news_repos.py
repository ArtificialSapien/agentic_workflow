from abc import ABC, abstractmethod
from typing import List

from data_model import NewsArticle


class NewsRepo(ABC):
    @abstractmethod
    def store(self, news_article: NewsArticle) -> None:
        pass

    @abstractmethod
    def load(self, article_id: str, source: str) -> NewsArticle:
        pass

    @abstractmethod
    def load_all(self, source: str) -> List[NewsArticle]:
        pass
