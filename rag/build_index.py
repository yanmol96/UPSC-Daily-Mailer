import os
import json
import faiss
from sentence_transformers import SentenceTransformer

from pdf_loader import load_pdf_text
from metadata_extractor import extract_metadata
from prelims_splitter import split_prelims_mcqs

DATA_DIR = "data/pyqs/prelims"
INDEX_DIR = "data/index"
os.makedirs(INDEX_DIR, exist_ok=True)

def build_index():
    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = []
    metadatas = []

    for file in os.listdir(DATA_DIR):
        if not file.endswith(".pdf"):
            continue

        pdf_path = os.path.join(DATA_DIR, file)
        print(f"[Index] {file}")

        pages = load_pdf_text(pdf_path)
        metadata = extract_metadata(pdf_path, pages)

        mcqs = split_prelims_mcqs(pages, metadata, verbose=False)

        for mcq in mcqs:
            combined = mcq["question"] + " " + " ".join(mcq["options"].values())
            texts.append(combined)
            metadatas.append(mcq)

    embeddings = model.encode(texts, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, f"{INDEX_DIR}/prelims.index")
    with open(f"{INDEX_DIR}/metadata.json", "w") as f:
        json.dump(metadatas, f, indent=2)

    print(f"[Index] Done. MCQs indexed: {len(metadatas)}")

if __name__ == "__main__":
    build_index()
