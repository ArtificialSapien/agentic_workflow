from strenum import StrEnum


class NewsProvider(StrEnum):
    ARXIV = "arxiv",
    GOOGLE = "google_news",
    MIT = "mit",
    WIRED = "wired"
