import re

GS_RE = re.compile(
    r'(GS\s*[1-4]|GENERAL STUDIES\s*[1-4]|PAPER\s*(I|II|III|IV))',
    re.I
)

def split_syllabus(raw_text):
    syllabus = []
    current_gs = None

    lines = [l.strip() for l in raw_text.split("\n") if l.strip()]

    for line in lines:
        # Detect GS paper
        gs_match = GS_RE.search(line)
        if gs_match:
            current_gs = normalize_gs(gs_match.group(0))
            continue

        # Ignore junk
        if len(line) < 8:
            continue

        syllabus.append({
            "gs": current_gs if current_gs else "UNKNOWN",
            "subject": infer_subject(line),
            "topic": clean_line(line)
        })

    return syllabus


def normalize_gs(text):
    t = text.upper()
    if "1" in t or "I" in t:
        return "GS1"
    if "2" in t or "II" in t:
        return "GS2"
    if "3" in t or "III" in t:
        return "GS3"
    if "4" in t or "IV" in t:
        return "GS4"
    return "UNKNOWN"


def clean_line(line):
    line = re.sub(r'^[•\-–—\d\.\)]*\s*', '', line)
    return line.strip()


def infer_subject(text):
    t = text.lower()

    if any(k in t for k in ["constitution", "parliament", "judiciary", "governance", "federal"]):
        return "polity"
    if any(k in t for k in ["economy", "growth", "inflation", "budget", "bank"]):
        return "economy"
    if any(k in t for k in ["environment", "forest", "biodiversity", "pollution", "ecology"]):
        return "environment"
    if any(k in t for k in ["climate", "monsoon", "weather"]):
        return "geography"
    if any(k in t for k in ["history", "culture", "art", "heritage"]):
        return "history"
    if any(k in t for k in ["science", "technology", "biotech", "space"]):
        return "science"
    if any(k in t for k in ["ethics", "integrity", "probity", "values"]):
        return "ethics"

    return "general"
