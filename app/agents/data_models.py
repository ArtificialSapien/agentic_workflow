from pydantic import BaseModel, Field
from typing import List


class NewsArticle(BaseModel):
    """Represents a news article"""

    title: str = Field(description="The title of the article")
    date: str = Field(description="The date of the article")
    content: str = Field(description="The content of the article")
    author: str = Field(description="The author of the article")
    source: str = Field(description="The source of the article")
    # query_api: str = Field(description="The API used to query the article")
    # query_prompt: str = Field(description="The prompt used to query the article")


class NewsArticles(BaseModel):
    """Represents a list of news articles"""

    articles: List[NewsArticle] = Field(description="The list of news articles")
