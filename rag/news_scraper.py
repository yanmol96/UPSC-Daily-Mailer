import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_article(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "lxml")

    title = soup.find("h1")
    title = title.get_text(strip=True) if title else ""

    paragraphs = soup.find_all("p")
    content = "\n".join(
        p.get_text(strip=True)
        for p in paragraphs
        if len(p.get_text(strip=True)) > 30
    )

    return {
        "title": title,
        "content": content
    }
