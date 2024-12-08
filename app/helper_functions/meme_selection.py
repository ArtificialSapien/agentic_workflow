import os
from langchain_google_genai import ChatGoogleGenerativeAI

from schemas.meme_selector_schema import MemeSelector

def meme_selection(prompt: str, templates):
    template_prompt = """
        You are an AI assistant. Given a user prompt, select the most appropriate meme template from the list below and provide only the template's ID and name. Do not return the entire list. The ID should be the number directly associated with the template.

        List of Templates:
        {templates}

        User Prompt: "{prompt}"

    """
    formatted_prompt = template_prompt.format(templates=templates, prompt=prompt)

        #enter api key
    api_key = os.getenv('GOOGLE_API_KEY')

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0.5,
        api_key=api_key
    )

    structure_llm = llm.with_structured_output(MemeSelector)
    response = structure_llm.invoke(formatted_prompt)
    return response

