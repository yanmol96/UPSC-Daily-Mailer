import os
import json
import faiss
import pickle
import pdfplumber
from sentence_transformers import SentenceTransformer

DATA_DIR = "data/pyqs/mains"
INDEX_DIR = "data/mains_pyq_index"

os.makedirs(INDEX_DIR, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []

def parse_pdf(pdf_path, gs_label):
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = [l.strip() for l in text.split("\n") if l.strip()]

            for line in lines:
                # crude but safe: skip headers
                if len(line) < 40:
                    continue

                documents.append({
                    "text": line,
                    "metadata": {
                        "gs": gs_label
                    }
                })


# ---- LOAD ALL GS PDFs ----
parse_pdf("data/pyqs/mains/GS1.pdf", "GS1")
parse_pdf("data/pyqs/mains/GS2.pdf", "GS2")
parse_pdf("data/pyqs/mains/GS3.pdf", "GS3")
parse_pdf("data/pyqs/mains/GS4.pdf", "GS4")

# ---- EMBEDDINGS ----
texts = [d["text"] for d in documents]
embeddings = model.encode(texts, show_progress_bar=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, f"{INDEX_DIR}/mains_pyq.index")

with open(f"{INDEX_DIR}/mains_pyq_meta.pkl", "wb") as f:
    pickle.dump(documents, f)

print(f"Indexed {len(documents)} mains PYQs")
