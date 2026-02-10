def assign_priority(title: str, syllabus_tags: list) -> str:
    title_l = title.lower()

    # --------------------
    # 1. HARD HIGH OVERRIDES (absolute UPSC core)
    # --------------------
    if any(x in title_l for x in [
        "supreme court", "constitutional", "article",
        "governor", "president", "assembly",
        "election commission", "cbi", "ed"
    ]):
        return "HIGH"

    # --------------------
    # 2. STRONG HIGH (keywords + GS II / III)
    # --------------------
    HIGH_KEYWORDS = [
        "budget", "economic survey", "inflation",
        "gdp", "monetary", "fiscal",
        "nuclear", "climate", "environment",
        "war", "treaty", "sanction", "foreign policy",
        "defence", "space"
    ]

    gs_core = any(
        "gs paper ii" in str(tag).lower() or
        "gs paper iii" in str(tag).lower()
        for tag in syllabus_tags
    )

    if gs_core and any(kw in title_l for kw in HIGH_KEYWORDS):
        return "HIGH"

    # --------------------
    # 3. MEDIUM PRIORITY BLOCK (important but not critical)
    # --------------------
    MEDIUM_KEYWORDS = [
        "party", "bjp", "congress", "leader",
        "resignation", "appointment", "reshuffle",
        "state unit", "political strategy",
        "sports", "culture", "heritage",
        "science explained", "knowledge nugget"
    ]

    if any(kw in title_l for kw in MEDIUM_KEYWORDS):
        return "MEDIUM"

    # --------------------
    # 4. LOW (everything else)
    # --------------------
    return "LOW"
