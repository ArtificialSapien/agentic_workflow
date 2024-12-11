import os
import json
from typing import List
from typing import TypedDict, Union
import requests

from app.models.base import AzureDallE3ImageGenerator, LangChainDallEImageGenerator
from app.agents.data_models import NewsArticle
from app.models.model_provider import ModelWrapper
from app.agents.data_models import NewsArticles, MemeTemplate, MemeCaptions

from app.helper_functions import fetch_templates
from app.helper_functions import ensure_markdown_format


from dotenv import load_dotenv

from app.web_crawler.news_sources import GoogleNewsSource
from app.web_crawler.query_encoder import QueryEncoder
from app.web_crawler.summarizers import Summarizer, SummarizerUsingGroq

# Load environment variables
load_dotenv(override=True)

# Initialize the image generator
if os.getenv("LLM_PROVIDER") == "openai":
    lim = LangChainDallEImageGenerator(api_key=os.getenv("OPENAI_API_KEY"))
else:
    lim = AzureDallE3ImageGenerator(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        url=os.getenv("AZURE_OPENAI_DALLE3_ENDPOINT"),
    )

# Initialize the LLM
model_wrapper = ModelWrapper.initialize_from_env()
llm = model_wrapper.model


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
    content_style: str
    content_format: str
    generate_text: bool
    generate_image: bool
    generate_video: bool
    generate_meme: bool
    news_articles: Union[NewsArticles, None]
    generated_text: Union[str, None]
    generated_image_url: Union[str, None]
    generated_video_url: Union[str, None]
    selected_meme_template: Union[MemeTemplate, None]
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
    user_prompt = state["user_prompt"]

    query_encoder = QueryEncoder()
    news_source = GoogleNewsSource()

    summarizer: Summarizer = SummarizerUsingGroq()

    topic = query_encoder.get_topic(state["user_prompt"])

    news_source.fetch({"q": topic, "engine": "google_news", "gl": "us", "hl": "en"})
    limit = os.getenv("MAX_NUMBER_OF_ARTICLES")
    complete_news_articles = news_source.get_news_content(limit=5)

    news_articles = []
    for news_article in complete_news_articles:
        short_text = summarizer.get_summary(str(news_article.content))
        news_article.content = short_text
        news_articles.append(news_article)

    # TODOD creates news articles
    # news_articles = load_json_files_from_folder("./data/work/wired/output")
    # news_articles = [NewsArticle(title="cooking class", date="today", content="this is a cooking class story", author="myself", source="whatever.com")]
    return {"news_articles": news_articles}


def text_generator(state: AgentState):
    """"""
    # TODOD creates posts
    """LangGraph node that will schedule tasks based on dependencies and team availability"""
    news_articles = state["news_articles"]
    user_prompt = state["user_prompt"]
    content_style = state["content_style"]
    content_format = state["content_format"]
    prompt = f"""
        You are a social media post creator. Use the provided news articles along
        with the initial user prompt used to collect the news articles to generate
        engaging social media text. Ensure the output reflects the specified format and style/tone.
        # Steps
            1. Review the provided news articles and the initial user prompt.
            2. Extract key points and themes from the articles.
            3. Craft a social media post that aligns with the desired style and tone.
            4. Format the output in Markdown, using appropriate headers, bullet points, and/ or links as needed.
        # Output Format'
            1. The output should be a single social media post formatted in Markdown.
            2. It should be written in the style and tone requested.
            3. It should have the length matching the requested style.
            4. Add references to the text extracted from the news articles field - 'source' in the text as an Markdown upper index at the end the corresponding sentence.
            5. Add all included references to the end of the post as a list of links using the matching indexing - appearance order in the text.
        **Given:**
            1. News Articles: {news_articles}
            2. User Prompt: {user_prompt}
            3. Expected article format: {content_format}
            4. Expected article style: {content_style}
        """
    if state["generate_text"] == True:
        try:
            generated_text: str = llm.invoke(prompt).content.strip()
        except Exception as e:
            generated_text = "LLM model invokation failed - please holder text"

        return {"generated_text": ensure_markdown_format(generated_text)}
    return {"generated_text": "Text generation was not requested"}


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
        return {"generated_image_url": ""}


def video_generator(state: AgentState):
    if state["generate_video"] == False:
        return {"generated_video_url": None}

    user_prompt = state["user_prompt"]
    initial_image_url = state["generated_image_url"]
    prompt = f"""
        You are a video creator.
        Given an initial image, your objective is to create a video using Stability AI.

        **Given:**
            - **Initial Image:** {initial_image_url}

        **Your objectives are to:**
            1. **Create:**
                - Create a video using Stability AI based on the initial image.
                - Enhance the visual quality and stability of the video.
                - Add relevant effects and transitions.
    """
    import requests

    response = requests.post(
        f"https://api.stability.ai/v2beta/image-to-video",
        headers={"authorization": f"""Bearer {os.getenv("STABILITY_AI_API_KEY")}"""},
        files={"image": open("../data/test_resized_image3.jpg", "rb")},
        data={"seed": 0, "cfg_scale": 1.8, "motion_bucket_id": 127},
    )

    print("Generation ID:", response.json().get("id"))

    return {"prompt": prompt}


def meme_selector(state: AgentState):
    if state["generate_meme"] == False:
        return {"selected_meme_template": None}

    user_prompt = state["user_prompt"]
    templates = fetch_templates()
    prompt = f"""
        Select the most appropriate meme template based on the provided user prompt: {user_prompt}
        Using the given list of templates: {templates}
        Each template is defined by a unique ID, name, URL, width, height, and box count.
        Your task is to analyze the user prompt to identify relevant keywords and themes,
        then match those with the best-fitting template from the list.

        # Steps
        1. **Analyze User Prompt**: Break down the user prompt to identify key themes and keywords.
        2. **Match Keywords with Templates**: Compare the identified keywords with the names of the templates to find the most relevant match.
        3. **Select Appropriate Template**: Choose the template that most closely aligns with the user's prompt.
        4. **Format the Output**: Structure the output to include the template's unique ID, name, URL, width, height, and box count.
    """
    structure_llm = llm.with_structured_output(MemeTemplate)
    selected_meme_template: MemeTemplate = structure_llm.invoke(prompt)
    return {"selected_meme_template": selected_meme_template}


def meme_generator(state: AgentState):
    if state["generate_meme"] == False:
        return {"generated_meme_url": None}

    user_prompt = state["user_prompt"]
    meme_template = state["selected_meme_template"]
    box_count = meme_template.box_count
    prompt = f"""
        You are an AI assistant. Given a user prompt and given meme template, select the
        most appropriate meme captions. The number of meme captions required will be based
        on the number of text boxes in the meme template {box_count}.

        User Prompt: "{user_prompt}"
        Meme Template: "{meme_template}"
        Box Counts: "{box_count}"

    """
    structure_llm = llm.with_structured_output(MemeCaptions)
    caption_response = structure_llm.invoke(prompt)

    template_id = meme_template.id
    username = os.getenv("IMGFLIP_USERNAME")
    password = os.getenv("IMGFLIP_PASSWORD")
    box_count = meme_template.box_count

    texts = []

    for i in range(box_count):
        texts.append(caption_response.captions[i])

    url = "https://api.imgflip.com/caption_image"

    # Prepare the payload with the parameters
    payload = {"template_id": template_id, "username": username, "password": password}

    for i in range(box_count):
        payload[f"text{i}"] = texts[i]

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            # Display the meme URL
            return {"generated_meme_url": data["data"]["url"]}
        else:
            return {"generated_meme_url": "failed to generate meme"}
    else:
        return {"generated_meme_url": "Failed to contact Imgflip API."}
