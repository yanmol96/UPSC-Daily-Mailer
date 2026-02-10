import faiss
from rag.embedder import Embedder
from rag.pdf_loader import load_pdf_text, chunk_text

class SyllabusRAG:
    def __init__(self, pdf_path):
        self.embedder = Embedder()
        pages = load_pdf_text(pdf_path)
        self.data = chunk_text(pages)

        texts = [d["text"] for d in self.data]
        self.embeddings = self.embedder.embed(texts)

        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(self.embeddings)

    def search(self, query, k=3):
        q_emb = self.embedder.embed(query)
        _, idx = self.index.search(q_emb, k)
        return [self.data[i] for i in idx[0]]
