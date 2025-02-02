import cloudscraper
from bs4 import BeautifulSoup
from app.agents.data_models import Date, Author, NewsArticle

from app.models.model_provider import ModelWrapper

from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)


# Initialize the LLM
model_wrapper = ModelWrapper.initialize_from_env()
llm = model_wrapper.model


def scrape_article(url: str) -> NewsArticle:
    scraper = cloudscraper.create_scraper()  # This creates a Cloudflare-scraper object
    response = scraper.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extracting the title
    title = soup.find("title").get_text()

    # Extracting the date (assuming there's a meta tag with name="date")
    date = (
        soup.find("meta", {"name": "date"})["content"]
        if soup.find("meta", {"name": "date"})
        else "Unknown"
    )

    # Extracting the content (assuming the article content is within <p> tags)
    content = " ".join([p.get_text() for p in soup.find_all("p")])

    # Extracting the author (assuming there's a meta tag with name="author")
    author = (
        soup.find("meta", {"name": "author"})["content"]
        if soup.find("meta", {"name": "author"})
        else "Unknown"
    )

    # Extracting the source (assuming the source is the domain of the URL)
    source = url.split("/")[2]

    structured_llm = llm.with_structured_output(Date)
    date: Date = structured_llm.invoke(f"""Extract date of content {content}""")
    structured_llm = llm.with_structured_output(Author)
    author: Author = structured_llm.invoke(
        f"""Extract author from the content {content}"""
    )

    return NewsArticle(
        title=title, date=date, content=content, author=author, source=source
    )
