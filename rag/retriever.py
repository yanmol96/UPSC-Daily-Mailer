import json
import faiss
from sentence_transformers import SentenceTransformer

from syllabus_linker import SyllabusLinker

INDEX_DIR = "data/index"


class PrelimsRetriever:
    def __init__(self):
        # Load PYQ FAISS index
        self.index = faiss.read_index(f"{INDEX_DIR}/prelims.index")

        # Load PYQ metadata
        with open(f"{INDEX_DIR}/metadata.json", "r") as f:
            self.metadata = json.load(f)

        # Embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Syllabus linker (LLM + embeddings)
        self.syllabus_linker = SyllabusLinker()

    def query(self, text, k=5, subject=None):
        """
        text: user query / topic / news headline
        k: number of results
        subject: optional subject filter (environment, polity, etc.)
        """

        # Embed query
        query_emb = self.model.encode([text])

        # Search PYQ index
        distances, indices = self.index.search(query_emb, k)

        results = []

        for idx in indices[0]:
            mcq = self.metadata[idx]

            # Optional subject filter
            if subject and mcq["subject"] != subject:
                continue

            # 🔥 Link syllabus (Stage C)
            mcq["syllabus_tags"] = self.syllabus_linker.link(
                mcq["question"]
            )

            results.append(mcq)

        return results
