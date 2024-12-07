from fastapi import FastAPI
from app.api.post_prompt import router as port_prompt_router

app = FastAPI()

app.include_router(port_prompt_router, tags=["post_prompt"], prefix="/post_prompt")



