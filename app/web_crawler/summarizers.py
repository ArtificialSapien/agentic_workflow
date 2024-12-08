import os

from abc import ABC, abstractmethod
from groq import Groq


class Summarizer(ABC):
    @abstractmethod
    def get_summary(self, text_to_summarize: str) -> str:
        pass


INCLUDE_TRANSFORMER_SUMMARIZER = False
if INCLUDE_TRANSFORMER_SUMMARIZER:
    from ktrain.text.summarization import TransformerSummarizer, LexRankSummarizer


    class SummarizerUsingKtrainTransformer(Summarizer):
        def __init__(self):
            self.__ts = TransformerSummarizer()

        def get_summary(self, text_to_summarize: str, min_length=100, max_length=150) -> str:
            summary = self.__ts.summarize(text_to_summarize, min_length=min_length, max_length=max_length)
            return summary


class SummarizerUsingGroq(Summarizer):
    def __init__(self):
        self.__client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def get_summary(self, text_to_summarize: str, min_length=100, max_length=150) -> str:
        try:
            chat_completion = self.__client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Summarize the following text with less than {min_length} words:

                        {text_to_summarize}

                        Return only a string of the summary without quotation mark, newline characters or other text.
                    """
                    }
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return ""
