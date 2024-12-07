from typing import TypedDict, Union

from langgraph.graph import StateGraph, START, END

from app.agents.nodes import web_crawler, text_generator, image_generator
from app.agents.data_models import NewsArticles


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


def create_post_creator_agent():
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

    return graph


def create_post(agent, initial_input):

    final_state = agent.invoke(initial_input)

    return (
        final_state["generated_text"],
        final_state["generated_image_url"],
        "whatever2",
        "whatever3",
    )
