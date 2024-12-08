# model_providers.py
from app.models.model_wrapper import ModelWrapper
from langchain_openai import AzureChatOpenAI, ChatOpenAI

# Register providers
ModelWrapper.register_provider("azure", AzureChatOpenAI)
ModelWrapper.register_provider("openai", ChatOpenAI)
