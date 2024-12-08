import requests

def fetch_templates():
    url = "https://api.imgflip.com/get_memes"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            return data["data"]["memes"]
        else:
            print("Failed to fetch meme templates.")
            return []
    else:
        print(f"HTTP Error: {response.status_code}")
        return []
