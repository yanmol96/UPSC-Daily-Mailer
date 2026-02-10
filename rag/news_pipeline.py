from news_loader import load_news_items
# from news_filter import NewsFilter
from news_summarizer import summarize_news
from retriever import PrelimsRetriever
from priority_classifier import assign_priority
from pyq_formatter import format_pyq_info
from mains_pyq_retriever import MainsPYQRetriever
from syllabus_linker import SyllabusLinker




class NewsPipeline:
    def __init__(self):
        # self.filter = NewsFilter()
        self.syllabus_linker = SyllabusLinker()
        self.retriever = PrelimsRetriever()
        self.mains_retriever = MainsPYQRetriever()


    # def _gate_pyqs(self, pyqs):
    #     """
    #     Soft gating:
    #     - If PYQs exist, keep top ones
    #     - No hard syllabus rejection
    #     """
    #     if not pyqs:
    #         return []

        
    #     # # keep top 3 by retriever score / order
    #     # return pyqs[:3]
    def _gate_pyqs(self, pyqs):
        """
        Aggregation mode:
        - Keep ALL PYQs
        - Formatting layer will summarize
        """
        return pyqs or []




    def _priority_score(self, syllabus_hits, pyqs):
        """
        Returns: High / Medium / Low
        """
        score = 0

        # Breadth
        score += len(syllabus_hits)

        # Historical importance
        if pyqs:
            score += 3

        # UPSC-favoured subjects
        subjects = " ".join(s["topic"].lower() for s in syllabus_hits)
        if any(x in subjects for x in ["environment", "polity", "economy"]):
            score += 2
        elif "ethics" in subjects or "society" in subjects:
            score += 1

        if score >= 6:
            return "HIGH"
        elif score >= 3:
            return "MEDIUM"
        return "LOW"

    def process(self, news_items, pyq_k=10):
        news_items = load_news_items(news_items)
        results = []

        for n in news_items:
            combined = n["title"] + " " + n["content"]

            # Step 1: syllabus relevance
            # syllabus_hits = self.filter.relevant_syllabus(combined)
            syllabus_hits = self.syllabus_linker.link(combined)
            if not syllabus_hits:
                continue

            # Step 2: retrieve PYQs
            prelims_pyqs = self.retriever.query(combined, k=pyq_k)
            mains_pyqs = self.mains_retriever.query(combined, k=pyq_k)
            print("DEBUG:", n["title"][:60])
            print("  Prelims PYQs:", len(prelims_pyqs))
            print("  Mains PYQs:", len(mains_pyqs))

            if prelims_pyqs:
                print("  Sample Prelims PYQ:", prelims_pyqs)

            if mains_pyqs:
                print("  Sample Mains PYQ:", mains_pyqs)

            # merge both
            raw_pyqs = prelims_pyqs + mains_pyqs


            # Step 3: gate PYQs
            gated_pyqs = self._gate_pyqs(raw_pyqs)
            # print("RAW PYQS:", len(raw_pyqs), "GATED:", len(gated_pyqs))


            # Step 4: priority score
            # Step 4: priority score
            priority = assign_priority(
                n["title"],
                syllabus_hits
            )



            # Step 5: summarize only if worth it
            # summary = summarize_news(combined)

            results.append({
                "title": n["title"],
                "source": n["source"],
                "url": n["url"],
                "priority": priority,
                "syllabus": syllabus_hits,
                "raw_text": combined,
                "related_pyqs": gated_pyqs,
                "pyq_info": format_pyq_info(gated_pyqs)
            })



        return results
