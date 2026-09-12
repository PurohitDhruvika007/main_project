from pathlib import Path
import pickle

import faiss
import numpy as np


VECTOR_DB_PATH = Path("data/vector_db")
INDEX_PATH = VECTOR_DB_PATH / "legal_documents.index"
TEXTS_PATH = VECTOR_DB_PATH / "legal_documents.pkl"


def create_vector_store(embeddings, texts):
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

    embeddings = np.asarray(embeddings, dtype="float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_PATH))

    with open(TEXTS_PATH, "wb") as file:
        pickle.dump(texts, file)

    return {
        "message": "Vector store created successfully",
        "total_vectors": index.ntotal,
        "dimension": dimension
    }


def load_vector_store():
    if not INDEX_PATH.exists() or not TEXTS_PATH.exists():
        raise FileNotFoundError("Vector store does not exist yet.")

    index = faiss.read_index(str(INDEX_PATH))

    with open(TEXTS_PATH, "rb") as file:
        texts = pickle.load(file)

    return index, texts


def search_similar_chunks(query_embedding, top_k=3):
    index, texts = load_vector_store()

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    scores, indices = index.search(query_embedding, top_k)

    results = []

    for score, index_position in zip(scores[0], indices[0]):
        if index_position == -1:
            continue

        results.append({
            "score": float(score),
            "text": texts[index_position]
        })

    return results
