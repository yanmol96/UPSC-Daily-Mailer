def load_news_items(news_items):
    """
    news_items: list of dicts
    [
      {
        "source": "The Hindu",
        "title": "...",
        "content": "...",
        "url": "https://..."
      },
      ...
    ]
    """

    cleaned = []

    for n in news_items:
        cleaned.append({
            "source": n.get("source", ""),
            "title": n["title"].strip(),
            "content": n["content"].strip(),
            "url": n.get("url", "")   # ✅ PRESERVE URL
        })

    return cleaned
