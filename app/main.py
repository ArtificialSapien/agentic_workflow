from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.generate_post import router as post_router
from app.api.finetune_text import router as finetunetext_router
from app.api.finetune_meme import router as finetunememe_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://0.0.0.0:8000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(post_router, tags=["post_prompt"], prefix="/post_prompt")
app.include_router(
    finetunetext_router, tags=["fine_tune_text"], prefix="/fine_tune_text"
)
app.include_router(
    finetunememe_router, tags=["fine_tune_meme"], prefix="/fine_tune_meme"
)

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
