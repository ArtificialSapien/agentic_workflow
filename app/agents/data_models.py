from pydantic import BaseModel, Field
from typing import List


class Date(BaseModel):
    year: int
    month: int
    day: int


class Author(BaseModel):
    name: str


class NewsArticle(BaseModel):
    """Represents a news article"""

    title: str = Field(description="The title of the article")
    date: Date = Field(description="The date of the article")
    content: str = Field(description="The content of the article")
    author: Author = Field(description="The author of the article")
    source: str = Field(description="The source of the article")


class NewsArticles(BaseModel):
    """Represents a list of news articles"""

    articles: List[NewsArticle] = Field(description="The list of news articles")


class MemeTemplate(BaseModel):
    id: str = Field(description="The ID of the meme template")
    name: str = Field(description="The name of the meme template")
    url: str = Field(description="The URL of the meme template")
    width: int = Field(description="The width of the meme template")
    height: int = Field(description="The height of the meme template")
    box_count: int = Field(description="The number of boxes in the meme template")


class MemeCaptions(BaseModel):
    captions: List[str] = Field(description="List of captions for the meme")
