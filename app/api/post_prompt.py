from fastapi import APIRouter, Depends
from app.schemas import response as schemas

from langchain_core.tools import tool
from langgraph.graph import StateGraph, START,END
from langchain_openai import AzureChatOpenAI

from typing import List, TypedDict
from pydantic import BaseModel, Field

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

router = APIRouter()

@router.post("/generate_post/", response_model=schemas.Response)
def generate_post(prompt: str):
    agent = create_agent()  
    initial_input = {"user_prompt": prompt, "news_articles": None, "generated_content": None}
    response = run_agent(agent = agent, initial_input = initial_input)

    return {"response": response}


llm = AzureChatOpenAI(deployment_name='gpt-4o-mini')

class NewsArticle(BaseModel):
    title: str = Field(description="The title of the article")
    date: str = Field(description="The date of the article")
    content: str = Field(description="The content of the article")
    author: str = Field(description="The author of the article")
    source: str = Field(description="The source of the article")

class NewsArticles(BaseModel):
    articles: List[NewsArticle] = Field(description="A list of news articles")


# Input: NewsArticle
# Prompt: 
class AgentState(TypedDict):
    user_prompt: str
    news_articles: NewsArticles
    generated_content: str  

def web_crawler(state: AgentState):
    """"""
    # TODOD creates news articles
    news_articles = [NewsArticle(title="cooking class", date="today", content="this is a cooking class story", author="myself", source="whatever.com")]
    return {"news_articles" : news_articles}

#def x_post_creator(news_article: NewsArticle):
#    """"""
#    # TODOD creates x-posts
#    return {"generated_content_text" : "generated_content_text"}

def post_generator(state: AgentState):
    """"""
    # TODOD creates posts
    """LangGraph node that will schedule tasks based on dependencies and team availability"""
    news_articles = state["news_articles"]
    user_prompt = state["user_prompt"]
    prompt = f"""
        You are a social media post creator.
        **Given:**
            - **News articles:** {news_articles}
        **Your objectives are to: **
            1. **Create:**
                - Create a social media post combining the information from each news article.
                - Add a title using the user prompt {user_prompt}.
        """
    generated_content: str = llm.invoke(prompt)
    return {"generated_content" : generated_content}


def create_agent():
    # Define a new graph
    workflow = StateGraph(AgentState)
    # Define the states
    workflow.add_node("web_crawler", web_crawler)
    workflow.add_node("post_generator", post_generator)
    # Define the transitions
    workflow.add_edge("web_crawler", "post_generator")
    # Define the start and end states
    workflow.add_edge(START, "web_crawler")
    workflow.add_edge("post_generator", END)
    # Return the graph

    agent = workflow.compile()

    return agent


def run_agent(agent,initial_input):
    print("Running agent")


    # Thread
    thread = {"configurable": {"thread_id": "1"}}

    # Run the graph until the first interruption
    for event in agent.stream(initial_input, thread, stream_mode="values"):
        print(event)
        # Do something here
        print("Agent finished")

    print(event['generated_content'].content)
    return (event['generated_content'].content)

