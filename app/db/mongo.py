from pymongo import MongoClient
from pydantic import BaseModel, Field

# Connect to the MongoDB server
client = MongoClient("localhost", 27017)
# Create or connect to a database
db = client.mydatabase
# Create or connect to a collection
collection = db.sessions


# Pydantic models
class Prompt(BaseModel):
    session_id: str = Field(description="The session ID")
    user_id: str = Field(description="The user ID")
    prompt: str = Field(description="The prompt")


class Response(BaseModel):
    session_id: str = Field(description="The session ID")
    user_id: str = Field(description="The user ID")
    response: str = Field(description="The response")
