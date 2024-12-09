from abc import ABC, abstractmethod
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
import requests


class ImageGeneratorAPI(ABC):
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        self.url = url
        self.image_url: str = None
        self.image_generated: bool = None

    @abstractmethod
    def generate_image(self, prompt: str) -> bytes:
        """Generate an image based on the given prompt."""
        pass

    def get_generated_images(self) -> str:
        """Helper method to make an API call."""
        if self.image_generated:
            return self.image_url

class LangChainDallEImageGenerator(ImageGeneratorAPI):
    """
    A LangChain-based DALL-E Image Generator extending the abstract ImageGeneratorAPI.
    """

    def __init__(self, api_key: str):
        """
        Initialize the LangChain DALL-E Image Generator.
        
        Args:
            api_key (str): OpenAI API key for authentication.
        """
        super().__init__(api_key, url=None)  # URL is managed by LangChain's DALL-E Wrapper
        self.dalle = DallEAPIWrapper(api_key=api_key)

    def generate_image(self, prompt: str, size: str = "1024x1024", n: int = 1) -> bytes:
        """
        Generate an image using the provided prompt.
        
        Args:
            prompt (str): The text prompt to generate an image.
            size (str): The size of the generated image (default: "1024x1024").
            n (int): The number of images to generate (default: 1).

        Returns:
            bytes: Binary content of the generated image.
        """
        try:
            response = self.dalle.run(prompt)
            if response:
                self.image_generated = True
                self.image_url = response
            else:
                self.image_generated = False
                self.image_url = None

        except Exception as e:
            self.image_generated = False
            self.image_url = None
            print(f"Error generating image: {e}")

    def get_generated_images(self) -> str:
        """
        Retrieve the URL of the last generated image.

        Returns:
            str: URL of the generated image or None if no image was generated.
        """
        return super().get_generated_images()



# Azure Dall-e-3 subclass for a specific image generation API
class AzureDallE3ImageGenerator(ImageGeneratorAPI):
    def __init__(self, api_key: str, url: str):
        super().__init__(api_key, url)

    def generate_image(self, prompt: str) -> None:

        headers = {"Content-Type": "application/json", "api-key": self.api_key}

        body = {
            "prompt": prompt,
            "size": "1024x1024",
            "n": 1,
            "quality": "standard",
            "style": "vivid",
        }

        response = requests.post(self.url, headers=headers, json=body)

        if response.status_code == 200:
            self.image_generated = True
            self.image_url = response.json()["data"][0]["url"]
        else:
            self.image_generated = False
