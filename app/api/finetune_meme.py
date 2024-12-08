from fastapi import APIRouter
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI

from app.schemas import response
from app.schemas import request

router = APIRouter()

llm = AzureChatOpenAI(deployment_name="gpt-4o-mini")


@router.post("/finetune_meme/", response_model=response.FineTunedMeme)
def finetune_meme(request: request.FineTuneRequest):
    pass  # TODO @Maaz
