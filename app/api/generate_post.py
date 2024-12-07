import os
import json
from typing import List

from fastapi import APIRouter
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI

from app.models.base import AzureDallE3ImageGenerator
from app.schemas import response
from app.schemas import request
from app.agents.post_creator import create_post_creator_agent, create_post

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
    agent = create_post_creator_agent()
    initial_input = {
        "user_prompt": initial_request.prompt,
        "generate_text": initial_request.generate_text,
        "generate_image": initial_request.generate_image,
        "generate_video": initial_request.generate_video,
        "generate_meme": initial_request.generate_meme,
    }
    generated_text, image_url, video_url, meme_url = create_post(
        agent=agent, initial_input=initial_input
    )

    return response.InitialResponse(
        generated_text=generated_text,
        image_url=image_url,
        video_url=video_url,
        meme_url=meme_url,
    )
