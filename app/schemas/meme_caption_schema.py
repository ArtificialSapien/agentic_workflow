from typing import List
from pydantic import BaseModel, Field

class MemeCaptions(BaseModel):
  captions: List[str] = Field(description="List of captions for the meme")