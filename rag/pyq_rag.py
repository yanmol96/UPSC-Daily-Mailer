import os
import re
import faiss
from rag.embedder import Embedder
from rag.pdf_loader import load_pdf_text, chunk_text
from rag.question_splitter import split_into_questions

class PYQRAG:
    def __init__(self, pyq_root):
        self.embedder = Embedder()
        self.data = []

        for exam in ["prelims"]:
            exam_path = os.path.join(pyq_root, exam)
            if not os.path.isdir(exam_path):
                continue

            for file in os.listdir(exam_path):
            # for file in ["PAPER I_2016.pdf"]:
                if not file.lower().endswith(".pdf"):
                    continue

                meta = self._parse_filename(file)
                if not meta:
                    continue

                pages = load_pdf_text(os.path.join(exam_path, file))
                chunks = chunk_text(pages, min_len=150)

                for c in chunks:
                    questions = split_into_questions(c["text"])
                    for q in questions:
                        self.data.append({
                            "text": q,
                            "page": c["page"],
                            **meta,
                            "source_pdf": file
                        })

        texts = [d["text"] for d in self.data]
        self.embeddings = self.embedder.embed(texts)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def _parse_filename(self, filename):
        name = filename.lower().replace(".pdf", "")
        year_match = re.search(r"(19|20)\d{2}", name)
        if not year_match:
            return None
        year = year_match.group(0)

        # PRELIMS
        if "paper_i" in name or "paper i" in name:
            return {"exam": "prelims", "paper": "GS",
                    "subject": None, "paper_no": "Paper1", "year": year}

        if "paper_ii" in name or "paper ii" in name:
            return {"exam": "prelims", "paper": "CSAT",
                    "subject": None, "paper_no": "Paper2", "year": year}

        # MAINS
        if "essay" in name:
            return {"exam": "mains", "paper": "Essay",
                    "subject": None, "paper_no": None, "year": year}

        if "english" in name:
            return {"exam": "mains", "paper": "English",
                    "subject": None, "paper_no": None, "year": year}

        gs_match = re.search(r"gs\s*([1-4])", name)
        if gs_match:
            return {"exam": "mains", "paper": f"GS{gs_match.group(1)}",
                    "subject": None, "paper_no": None, "year": year}

        opt_match = re.search(r"optional[_\s]+(.+?)[_\s]+paper\s*(i|ii)", name)
        if opt_match:
            return {
                "exam": "mains",
                "paper": "Optional",
                "subject": opt_match.group(1).title(),
                "paper_no": "Paper1" if opt_match.group(2) == "i" else "Paper2",
                "year": year
            }

        return None

    def search(self, query, k=5, **filters):
        q_emb = self.embedder.embed(query)
        _, idx = self.index.search(q_emb, k * 5)
        results = [self.data[i] for i in idx[0]]

        for key, value in filters.items():
            results = [r for r in results if r.get(key) == value]

        return results[:k]
