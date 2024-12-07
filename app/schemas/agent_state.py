from typing import TypedDict, Union
from app.schemas.data_models import NewsArticles

# Input: NewsArticle
# Prompt: 
class AgentState(TypedDict):
    user_prompt: str
    generate_text: bool
    generate_image: bool
    generate_video: bool
    generate_meme: bool
    news_articles: Union[NewsArticles, None]
    generated_text: Union[str, None]
    generated_image_url: Union[str, None]
    generated_video_url: Union[str, None]
    generated_meme_url: Union[str, None]