import os
import re

YEAR_RE = re.compile(r'(19|20)\d{2}')

def extract_metadata(pdf_path, pages):
    # subject from filename
    filename = os.path.basename(pdf_path)
    subject = os.path.splitext(filename)[0].lower()

    # year from first 2 pages
    text = " ".join(p["text"] for p in pages[:2])
    year_match = YEAR_RE.search(text)
    year = int(year_match.group()) if year_match else None

    return {
        "exam": "prelims",
        "paper": "GS1",
        "subject": subject,
        "year": year
    }
