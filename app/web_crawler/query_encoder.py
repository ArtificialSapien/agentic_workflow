import os

from groq import Groq


class QueryEncoder:
    def __init__(self):
        self.__client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def get_topic(self, prompt: str) -> str:
        chat_completion = self.__client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                        Provide an input for a google news search query based on the following prompt:
                        
                        {prompt}
                        
                        Return only a string with the topic. No other text is required. Do not add quotation marks.
                    """
                }
            ],
            model="llama3-8b-8192",
        )
        topic = str(chat_completion.choices[0].message.content)
        print(topic)
        topic = topic.replace('\n', '')
        topic = topic.replace('"', '')
        topic = topic.replace("'", '')
        return topic
