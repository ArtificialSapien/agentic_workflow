import os
import json
from typing import List

from fastapi import APIRouter
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI

from app.models.base import AzureDallE3ImageGenerator
from app.schemas import response
from app.schemas import request
from app.schemas.data_models import NewsArticle
from app.schemas.agent_state import AgentState

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

router = APIRouter()


@router.post("/generate_post/", response_model=response.InitialResponse)
def generate_post(
    initial_request: request.InitialRequest,
    # user_id: str,
    # session_id: str,
    # prompt: str,
    # generate_text: bool,
    # generate_image: bool,
    # generate_video: bool,
    # generate_meme: bool
):
    agent = create_agent()
    initial_input = {
        "user_prompt": initial_request.prompt,
        "generate_text": initial_request.generate_text,
        "generate_image": initial_request.generate_image,
        "generate_video": initial_request.generate_video,
        "generate_meme": initial_request.generate_meme,
    }
    generated_text, image_url, video_url, meme_url = run_agent(
        agent=agent, initial_input=initial_input
    )

    return response.InitialResponse(
        generated_text=generated_text,
        image_url=image_url,
        video_url=video_url,
        meme_url=meme_url,
    )


llm = AzureChatOpenAI(deployment_name="gpt-4o-mini")
lim = AzureDallE3ImageGenerator(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    url=os.getenv("AZURE_OPENAI_DALLE3_ENDPOINT"),
)


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
    generated_text: str = llm.invoke(prompt).content
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
            return {"generated_image_url": "No image generated due to internal error"}

    else:
        return {"generated_image_url": "Image generation was not requested"}


def create_agent():
    # Define a new graph
    workflow = StateGraph(AgentState)
    # Define the states
    workflow.add_node("web_crawler", web_crawler)
    workflow.add_node("text_generator", text_generator)
    workflow.add_node("image_generator", image_generator)
    # Define the transitions
    workflow.add_edge("web_crawler", "text_generator")
    workflow.add_edge("web_crawler", "image_generator")
    # Define the start and end states
    workflow.add_edge(START, "web_crawler")
    workflow.add_edge("text_generator", END)
    workflow.add_edge("image_generator", END)
    # Return the graph

    graph = workflow.compile()

    # View
    # display(Image(graph.get_graph().draw_mermaid_png()))

    return graph


def run_agent(agent, initial_input):

    final_state = agent.invoke(initial_input)

    return (
        final_state["generated_text"],
        final_state["generated_image_url"],
        "whatever2",
        "whatever3",
    )
