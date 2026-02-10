from daily_news_pipeline import DailyNewsPipeline
from email_sender import send_email
from email_formatter import format_daily_email
from datetime import date

TO_EMAIL = "lakshyayadav3009.ly@gmail.com"

pipeline = DailyNewsPipeline()
results = pipeline.run()

if results:
    html = format_daily_email(results)
    subject = f"UPSC Daily Current Affairs – {date.today().isoformat()}"
    send_email(TO_EMAIL, subject, html)
