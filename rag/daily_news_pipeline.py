from rss_fetcher import fetch_rss_articles
from news_scraper import scrape_article
from news_pipeline import NewsPipeline
from news_summarizer import summarize_news

RSS_FEEDS = [
    "https://indianexpress.com/feed/",
    "https://www.thehindu.com/news/feeder/default.rss"
]


class DailyNewsPipeline:
    def __init__(self, per_feed_limit=40, top_k=10):
        self.per_feed_limit = per_feed_limit
        self.top_k = top_k
        self.pipeline = NewsPipeline()

    def run(self):
        scraped_news = []

        # ---------------------------
        # STEP A: RSS + SCRAPE
        # (NO keyword filtering here)
        # ---------------------------
        for feed in RSS_FEEDS:
            entries = fetch_rss_articles(feed, self.per_feed_limit)

            for e in entries:
                try:
                    article = scrape_article(e["link"])

                    # if len(article["content"]) < 500:
                    #     continue

                    scraped_news.append({
                        "source": e["source"],
                        "title": article["title"],
                        "content": article["content"],
                        "url": e["link"]     # ✅ IMPORTANT
                    })

                except Exception:
                    continue

        # ---------------------------
        # STEP B: syllabus + PYQ + priority
        # ---------------------------
        results = self.pipeline.process(scraped_news)

        # ---------------------------
        # STEP C: priority sort
        # ---------------------------
        priority_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        results.sort(
            key=lambda x: priority_order.get(x["priority"], 0),
            reverse=True
        )

        final_results = []

        for r in results:
            if r["priority"] == "LOW":
                continue

            # HIGH + MEDIUM both get LLM material
            r["summary"] = summarize_news(r["raw_text"])
            r["pyq_status"] = r.get("pyq_info", "—")

            del r["raw_text"]
            final_results.append(r)

            if len(final_results) >= self.top_k:
                break

        return final_results
