from fastapi import APIRouter
from langgraph.graph import StateGraph, START, END
from langchain_openai import AzureChatOpenAI

from app.schemas import response
from app.schemas import request
from app.schemas.agent_state import AgentState

router = APIRouter()

llm = AzureChatOpenAI(deployment_name='gpt-4o-mini')

@router.post("/finetune_post/", response_model=response.FineTunedText)
def finetune_text(request: request.FineTuneRequest):

    prompt = f"""
    You are an advanced language model. Your task is to update the previous LLM response to better address the new prompt. Follow these steps:

    1. Carefully read the new prompt and the previous LLM response.
    2. Identify any gaps or areas where the previous response does not fully address the new prompt.
    3. Update the response to ensure it is coherent, accurate, and directly relevant to the new prompt.
    4. Maintain a professional and informative tone.

    New Prompt: {request.prompt}

    Previous LLM Response: {request.generated_text}

    Now, update the response based on the new prompt provided.

    Updated Response:
    """
    finetuned_text = llm.invoke(prompt).content

    return response.FineTunedText(generated_text=finetuned_text)

