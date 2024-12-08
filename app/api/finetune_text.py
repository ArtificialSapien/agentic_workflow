from fastapi import APIRouter

from app.models.model_provider import ModelWrapper
from app.schemas import response
from app.schemas import request

router = APIRouter()

# Initialize the LLM
model_wrapper = ModelWrapper.initialize_from_env()
llm = model_wrapper.model


@router.post("/finetune_post/", response_model=response.FineTunedText)
def finetune_text(request: request.FineTuneTextRequest):

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
