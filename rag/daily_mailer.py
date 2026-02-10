from daily_news_pipeline import DailyNewsPipeline
from email_sender import send_email
from email_formatter import format_daily_email
from datetime import date

TO_EMAIL = "lakshyayadav3009.ly@gmail.com"

pipeline = DailyNewsPipeline()
results = pipeline.run()

if results:from daily_news_pipeline import DailyNewsPipeline
from email_sender import send_email
from email_formatter import format_daily_email
from datetime import date

TO_EMAILS = [
    "lakshyayadav3009.ly@gmail.com",
    "yanmol1403@gmail.com"
]

pipeline = DailyNewsPipeline()
results = pipeline.run()   # ← processed ONLY ONCE

if results:
    html = format_daily_email(results)
    subject = f"UPSC Daily Current Affairs – {date.today().isoformat()}"

    for email in TO_EMAILS:
        send_email(email, subject, html)

    html = format_daily_email(results)
    subject = f"UPSC Daily Current Affairs – {date.today().isoformat()}"
    send_email(TO_EMAIL, subject, html)
