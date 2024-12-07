from pydantic import BaseModel

class InitialRequest(BaseModel):
    prompt: str
    text: bool
    image: bool
    video: bool
    audio: bool