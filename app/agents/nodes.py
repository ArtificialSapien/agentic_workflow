import os
import json
from typing import List
from typing import TypedDict, Union

from langchain_openai import AzureChatOpenAI

from app.models.base import AzureDallE3ImageGenerator
from app.agents.data_models import NewsArticle
from app.models.model_provider import ModelWrapper
from app.agents.data_models import NewsArticles


from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

llm = AzureChatOpenAI(deployment_name="gpt-4o-mini")
lim = AzureDallE3ImageGenerator(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    url=os.getenv("AZURE_OPENAI_DALLE3_ENDPOINT"),
)

# Initialize the LLM
# model_wrapper = ModelWrapper.initialize_from_env()
# llm = model_wrapper.model

class AgentState(TypedDict):
    """
    Represents the state of an agent.

    Attributes:
        user_prompt (str): The prompt provided by the user.
        generate_text (bool): Indicates whether text generation is enabled.
        generate_image (bool): Indicates whether image generation is enabled.
        generate_video (bool): Indicates whether video generation is enabled.
        generate_meme (bool): Indicates whether meme generation is enabled.
        news_articles (Union[NewsArticles, None]): The news articles used for generation.
        generated_text (Union[str, None]): The generated text.
        generated_image_url (Union[str, None]): The URL of the generated image.
        generated_video_url (Union[str, None]): The URL of the generated video.
        generated_meme_url (Union[str, None]): The URL of the generated meme.
    """

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

def load_json_files_from_folder(folder_path: str) -> List[NewsArticle]:
    articles = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                article = NewsArticle(**data)
                articles.append(article)
    return articles


def web_crawler(state: AgentState):
    """"""
    # TODOD creates news articles
    news_articles = load_json_files_from_folder("./data/work/wired/output")
    # news_articles = [NewsArticle(title="cooking class", date="today", content="this is a cooking class story", author="myself", source="whatever.com")]
    return {"news_articles": news_articles}


def text_generator(state: AgentState):
    """"""
    # TODOD creates posts
    """LangGraph node that will schedule tasks based on dependencies and team availability"""
    news_articles = state["news_articles"]
    user_prompt = state["user_prompt"]
    prompt = f"""
        You are a social media post creator.
        **Given:**
            - **News articles:** {news_articles}
            - **User prompt:** {user_prompt}
        **Your objectives are to: **
            1. **Create:**
                - Create a social media post combining the information from each news article.
                - Add a title using the user prompt {user_prompt}.
        """
    try:
        generated_text: str = llm.invoke(prompt).content
    except Exception as e:
        generated_text = "LLM model invokation failed - please holder text"
    return {"generated_text": generated_text}


def image_generator(state: AgentState):
    """"""
    # TODOD creates posts
    """LangGraph node that will schedule tasks based on dependencies and team availability"""
    news_articles = state["news_articles"]
    user_prompt = state["user_prompt"]
    prompt_for_instructing_image_generation = f"""
        You are a social media post creator.
        **Given:**
            - **News articles:** {news_articles}
            - **User prompt:** {user_prompt}
        **Your objectives are to: **
            1. **Create:**
                - Create a prompt based on the received news articles and initial user prompt to instruct the image generator to create an image.
                - Ensure that the style, content are aligned with the provided context.
        """
    if state["generate_image"] == True:

        try:
            prompt_for_image_generation: str = llm.invoke(
                prompt_for_instructing_image_generation
            ).content
            print(prompt_for_image_generation)

            # Call the image generator API
            lim.generate_image(prompt_for_image_generation)
            if lim.image_generated:
                print("image_was_generated")
                return {"generated_image_url": lim.image_url}
            else:
                return {
                    "generated_image_url": "No image generated due to internal error"
                }
        except Exception as e:
            return {"generated_image_url": "Certain error occured"}

    else:
        return {"generated_image_url": "Image generation was not requested"}
