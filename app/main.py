from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.generate_post import router as port_prompt_router
from app.api.finetune_text import router as fine_tune_prompt_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust origin as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(port_prompt_router, tags=["post_prompt"], prefix="/post_prompt")
app.include_router(
    fine_tune_prompt_router, tags=["fine_tune_prompt"], prefix="/fine_tune_prompt"
)
