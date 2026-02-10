import json
from pdf_loader import load_pdf_text
from syllabus_splitter import split_syllabus

def build_syllabus_store(pdf_path, out_path="data/clean_syllabus.json"):
    pages = load_pdf_text(pdf_path)
    full_text = "\n".join(p["text"] for p in pages)

    syllabus = split_syllabus(full_text)

    with open(out_path, "w") as f:
        json.dump(syllabus, f, indent=2)

    print(f"Saved {len(syllabus)} syllabus entries to {out_path}")
