from typing import List
from pydantic import BaseModel, Field

class MemeSelector(BaseModel):
  id: str = Field(description="The ID of the meme template")
  name: str = Field(description="The name of the meme template")
  url: str = Field(description="The URL of the meme template")
  width: int = Field(description="The width of the meme template")
  height: int = Field(description="The height of the meme template")
  box_count: int = Field(description="The number of boxes in the meme template")

