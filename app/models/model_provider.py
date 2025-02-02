# model_providers.py
from app.models.model_wrapper import ModelWrapper
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from app.models.base import AIMLAPIImageGenerator

# Register providers
ModelWrapper.register_provider("azure", AzureChatOpenAI)
ModelWrapper.register_provider("openai", ChatOpenAI)
ModelWrapper.register_provider("gemini", ChatGoogleGenerativeAI)
ModelWrapper.register_provider("groq", ChatGroq)
ModelWrapper.register_provider("aimlapi", AIMLAPIImageGenerator)
