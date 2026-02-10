# def format_pyq_info(pyqs):
#     if not pyqs:
#         return "No direct PYQ; conceptually relevant"

#     years = sorted(set(q.get("year") for q in pyqs if q.get("year")))
#     papers = sorted(set(q.get("paper") for q in pyqs if q.get("paper")))

#     return f"PYQs asked in {', '.join(papers)} ({', '.join(map(str, years))})"

import re

YEAR_RE = re.compile(r'\b(19\d{2}|20\d{2})\b')

def extract_year_from_text(text: str):
    if not text:
        return None
    m = YEAR_RE.search(text)
    return m.group(0) if m else None


def format_pyq_info(pyqs):
    if not pyqs:
        return "Conceptually relevant (no direct PYQ)"

    prelims_years = set()
    prelims_papers = set()

    mains_years = set()
    mains_papers = set()

    for q in pyqs:
        # -------- PRELIMS --------
        if q.get("exam") == "prelims":
            if q.get("paper"):
                prelims_papers.add(q["paper"])
            if q.get("year"):
                prelims_years.add(str(q["year"]))

        # -------- MAINS --------
        if "metadata" in q:
            gs = q["metadata"].get("gs")
            if gs:
                mains_papers.add(gs)

            # 🔥 extract year from question text
            year = extract_year_from_text(q.get("text", ""))
            if year:
                mains_years.add(year)

    parts = []

    if prelims_papers:
        parts.append(
            f"Prelims: {', '.join(sorted(prelims_papers))}"
            + (f" ({', '.join(sorted(prelims_years))})" if prelims_years else "")
        )

    if mains_papers:
        parts.append(
            f"Mains: {', '.join(sorted(mains_papers))}"
            + (f" ({', '.join(sorted(mains_years))})" if mains_years else "")
        )

    return " | ".join(parts)
