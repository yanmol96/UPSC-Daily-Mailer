class SyllabusLinker:
    def link(self, text):
        text_l = text.lower()
        hits = []

        def add(gs, topic, subject):
            hits.append({
                "gs": gs,
                "topic": topic,
                "subject": subject
            })

        # ---------------- GS2 ----------------
        if any(k in text_l for k in [
            "governor", "supreme court", "high court",
            "constitution", "parliament", "judiciary",
            "election commission", "article", "bill"
        ]):
            add("GS2", "Polity and Governance", "polity")

        if any(k in text_l for k in [
            "foreign", "bilateral", "summit", "treaty",
            "united nations", "usa", "china", "pakistan",
            "israel", "gaza", "ukraine"
        ]):
            add("GS2", "International Relations", "ir")

        # ---------------- GS3 ----------------
        if any(k in text_l for k in [
            "economy", "budget", "inflation", "gdp",
            "bank", "rbi", "fiscal", "monetary"
        ]):
            add("GS3", "Indian Economy", "economy")

        if any(k in text_l for k in [
            "climate", "environment", "pollution",
            "forest", "biodiversity"
        ]):
            add("GS3", "Environment", "environment")

        if any(k in text_l for k in [
            "nuclear", "missile", "defence", "security",
            "terror", "cyber"
        ]):
            add("GS3", "Internal Security", "security")

        # ---------------- GS4 ----------------
        if any(k in text_l for k in [
            "ethics", "values", "integrity",
            "corruption", "probity"
        ]):
            add("GS4", "Ethics in Governance", "ethics")

        # ❌ Drop article if nothing maps
        if not hits:
            return None

        return hits
