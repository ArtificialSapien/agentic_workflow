from abc import ABC, abstractmethod
import requests

class ImageGeneratorAPI(ABC):
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        self.url = url
        self.image_url: str =  None
        self.image_generated: bool = None

    @abstractmethod
    def generate_image(self, prompt: str) -> bytes:
        """Generate an image based on the given prompt."""
        pass


    def get_generated_images(self) -> str:
        """Helper method to make an API call."""
        if self.image_generated:
            return self.image_url
    

# Azure Dall-e-3 subclass for a specific image generation API
class AzureDallE3ImageGenerator(ImageGeneratorAPI):
    def __init__(self, api_key: str, url: str):
        super().__init__(api_key, url)
    
    def generate_image(self, prompt: str) -> None:
          
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }

        body = {
            "prompt": prompt,
            "size": "1024x1024", 
            "n": 1,
            "quality": "hd", 
            "style": "vivid"
        }

        response = requests.post(self.url, headers=headers, json=body)
        
        if response.status_code == 200:
            self.image_generated = True
            self.image_url = response.json()['data'][0]['url']
        else:
            self.image_generated = False