import json
import faiss
from sentence_transformers import SentenceTransformer

SYLLABUS_DIR = "data/syllabus_index"

class NewsFilter:
    def __init__(self, k=3, threshold=1.2):
        self.k = k
        self.threshold = threshold
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(f"{SYLLABUS_DIR}/syllabus.index")

        with open(f"{SYLLABUS_DIR}/syllabus_metadata.json") as f:
            self.syllabus = json.load(f)

    def relevant_syllabus(self, text):
        emb = self.model.encode([text])
        D, I = self.index.search(emb, self.k)

        hits = []
        for dist, idx in zip(D[0], I[0]):
            if dist < self.threshold:
                hits.append(self.syllabus[idx])

        return hits
