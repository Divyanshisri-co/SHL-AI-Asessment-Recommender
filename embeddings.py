import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


CATALOG_PATH = "data/shl_catalog.json"
INDEX_PATH = "data/shl_index.faiss"
METADATA_PATH = "data/metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_catalog():
    if not os.path.exists(CATALOG_PATH):
        raise FileNotFoundError(
            "Catalog not found. Run scraper.py first."
        )

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_document(item):
    """
    Create searchable text from catalog item
    """
    text = f"""
    Name: {item.get('name', '')}
    Description: {item.get('description', '')}
    Skills: {' '.join(item.get('skills', []))}
    Type: {item.get('test_type', '')}
    URL: {item.get('url', '')}
    """
    return text.strip()


def create_embeddings():
    catalog = load_catalog()

    if not catalog:
        raise ValueError("Catalog is empty.")

    print("Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    docs = []
    metadata = []

    for item in catalog:
        doc = build_document(item)
        docs.append(doc)

        metadata.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"],
            "description": item["description"],
            "skills": item["skills"]
        })

    print("Generating embeddings...")
    embeddings = model.encode(
        docs,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype("float32")

    dimension = embeddings.shape[1]

    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("Embeddings created successfully.")
    print(f"Index saved: {INDEX_PATH}")
    print(f"Metadata saved: {METADATA_PATH}")


if __name__ == "__main__":
    create_embeddings()