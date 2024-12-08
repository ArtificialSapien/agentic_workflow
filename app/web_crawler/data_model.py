from pydantic import BaseModel, Field

class NewsArticle(BaseModel):
    title: str = Field(description="The title of the article")
    date: str = Field(description="The date of the article")
    content: str = Field(description="The content of the article")
    author: str = Field(description="The author of the article")
    source: str = Field(description="The source of the article")
