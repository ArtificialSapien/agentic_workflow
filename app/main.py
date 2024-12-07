from fastapi import FastAPI
from app.api.generate_post import router as port_prompt_router
from app.api.finetune_text import router as fine_tune_prompt_router

app = FastAPI()

app.include_router(port_prompt_router, tags=["post_prompt"], prefix="/post_prompt")
app.include_router(fine_tune_prompt_router, tags=["fine_tune_prompt"], prefix="/fine_tune_prompt")

