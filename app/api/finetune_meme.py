from fastapi import APIRouter
from app.models.model_provider import ModelWrapper

import requests

from app.schemas import response
from app.schemas import request
from app.schemas.response import Meme

from app.agents.data_models import MemeCaptions

router = APIRouter()

# Initialize the LLM
model_wrapper = ModelWrapper.initialize_from_env()
llm = model_wrapper.model


@router.post("/finetune_meme/", response_model=response.Meme)
def finetune_meme(request: request.FineTuneMemeRequest):
    user_prompt = request.prompt
    meme_template = request.meme.meme_template
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
    username = "mmaazkhanhere"
    password = "HelloWorld00."
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
            return Meme(meme_template=meme_template, meme_url=data["data"]["url"])
        else:
            return Meme(
                meme_template=meme_template, meme_url="Failed to generate meme."
            )
    else:
        return Meme(
            meme_template=meme_template, meme_url="Failed to contact Imgflip API."
        )
