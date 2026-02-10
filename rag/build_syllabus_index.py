import os
import json
import faiss
from sentence_transformers import SentenceTransformer

from syllabus_pdf_loader import load_syllabus_pdf
from syllabus_splitter import split_syllabus

INDEX_DIR = "data/syllabus_index"
os.makedirs(INDEX_DIR, exist_ok=True)

def build_syllabus_index(pdf_path):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    raw_text = load_syllabus_pdf(pdf_path)
    syllabus = split_syllabus(raw_text)

    texts = [s["topic"] for s in syllabus]
    embeddings = model.encode(texts, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, f"{INDEX_DIR}/syllabus.index")

    with open(f"{INDEX_DIR}/syllabus_metadata.json", "w") as f:
        json.dump(syllabus, f, indent=2)

    print(f"[Syllabus] Indexed {len(syllabus)} syllabus points")


if __name__ == "__main__":
    build_syllabus_index("data/syllabus/syllabus.pdf")
