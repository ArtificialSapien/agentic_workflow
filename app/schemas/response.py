from pydantic import BaseModel

class InitialResponse(BaseModel):
    generated_text: str
    image_url: str
    video_url: str
    meme_url: str

class FineTunedText(BaseModel):
    generated_text: str

class FineTunedImage(BaseModel):
    image_url: str

class FineTunedVideo(BaseModel):
    video_url: str

class FineTunedMeme(BaseModel):
    meme_url: str


