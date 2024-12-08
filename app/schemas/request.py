from pydantic import BaseModel, Field
from app.schemas.response import Meme


class InitialRequest(BaseModel):
    # user_id: str = Field(description="The user ID")  # Potential field to add
    # session_id: str = Field(description="The session ID") # Potential field to add
    prompt: str = Field(description="The prompt")
    format: str = Field(
        default="linkedin", description="The format of the generated content"
    )
    style: str = Field(
        default="professional", description="The style of the generated content"
    )
    generate_text: bool = Field(default=True, description="Flag whether generate text")
    generate_image: bool = Field(
        default=False, description="Flag whether generate image"
    )
    generate_video: bool = Field(
        default=False, description="Flag whether generate video"
    )
    generate_meme: bool = Field(default=False, description="Flag whether generate meme")


class FineTuneTextRequest(BaseModel):
    # user_id: str = Field(description="The user ID")  # Potential field to add
    # session_id: str = Field(description="The session ID") # Potential field to add
    prompt: str = Field(description="The prompt")
    generated_text: str = Field(
        description="The generated text component of the social media post"
    )


class FineTuneMemeRequest(BaseModel):
    # user_id: str = Field(description="The user ID")  # Potential field to add
    # session_id: str = Field(description="The session ID") # Potential field to add
    prompt: str = Field(description="The prompt")
    meme: Meme = Field(description="The meme component of the social media post")
