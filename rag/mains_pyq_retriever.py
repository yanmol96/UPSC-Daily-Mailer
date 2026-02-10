import faiss
import pickle
from sentence_transformers import SentenceTransformer

INDEX_DIR = "data/mains_pyq_index"

class MainsPYQRetriever:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(f"{INDEX_DIR}/mains_pyq.index")

        with open(f"{INDEX_DIR}/mains_pyq_meta.pkl", "rb") as f:
            self.meta = pickle.load(f)

    def query(self, text, k=5):
        emb = self.model.encode([text])
        _, I = self.index.search(emb, k)

        results = []
        for i in I[0]:
            results.append(self.meta[i])

        return results
