import feedparser

def fetch_rss_articles(feed_url, limit=50):
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:limit]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "source": feed.feed.get("title", "")
        })

    return articles
