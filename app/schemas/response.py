from pydantic import BaseModel
from app.agents.data_models import MemeTemplate


class Meme(BaseModel):
    meme_template: MemeTemplate
    meme_url: str


class InitialResponse(BaseModel):
    generated_text: str
    image_url: str
    video_url: str
    meme: Meme


class FineTunedText(BaseModel):
    generated_text: str


class FineTunedImage(BaseModel):
    image_url: str


class FineTunedVideo(BaseModel):
    video_url: str
