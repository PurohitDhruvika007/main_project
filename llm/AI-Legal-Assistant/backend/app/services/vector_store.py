from pathlib import Path
import pickle
import uuid

import faiss
import numpy as np


VECTOR_DB_PATH = Path("data/vector_db")

INDEX_PATH = VECTOR_DB_PATH / "legal_documents.index"
TEXTS_PATH = VECTOR_DB_PATH / "legal_documents.pkl"


def create_vector_store(
    embeddings,
    texts,
    document_id=None,
    filename=None
):
    VECTOR_DB_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    if embeddings.ndim != 2:
        raise ValueError(
            "Embeddings must be a 2-dimensional array."
        )

    if len(embeddings) == 0:
        raise ValueError(
            "No embeddings were generated."
        )

    if len(texts) != len(embeddings):
        raise ValueError(
            "Number of texts and embeddings must match."
        )

    if document_id is None:
        document_id = uuid.uuid4().hex

    dimension = embeddings.shape[1]

    # Create a new FAISS index
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    # Store metadata with every chunk
    records = []

    for text in texts:
        records.append({
            "document_id": document_id,
            "filename": filename,
            "text": text
        })

    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    with open(
        TEXTS_PATH,
        "wb"
    ) as file:

        pickle.dump(
            records,
            file
        )

    return {
        "message": "Vector store created successfully",
        "document_id": document_id,
        "total_vectors": index.ntotal,
        "dimension": dimension
    }


def load_vector_store():

    if (
        not INDEX_PATH.exists()
        or not TEXTS_PATH.exists()
    ):
        raise FileNotFoundError(
            "Vector store does not exist yet."
        )

    index = faiss.read_index(
        str(INDEX_PATH)
    )

    with open(
        TEXTS_PATH,
        "rb"
    ) as file:

        records = pickle.load(file)

    return index, records


def search_similar_chunks(
    query_embedding,
    top_k=3,
    document_id=None
):

    index, records = load_vector_store()

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    ).reshape(1, -1)

    if index.ntotal == 0:
        return []

    # Search more results when filtering by document
    search_k = index.ntotal

    scores, indices = index.search(
        query_embedding,
        search_k
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        record = records[index_position]

        # If document_id is provided,
        # return only chunks from that document.
        if (
            document_id is not None
            and record.get("document_id") != document_id
        ):
            continue

        results.append({
            "score": float(score),
            "document_id": record.get(
                "document_id"
            ),
            "filename": record.get(
                "filename"
            ),
            "text": record.get(
                "text",
                ""
            )
        })

        if len(results) >= top_k:
            break

    return results
