import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from src.chunking import create_chunks
from src.document_loader import load_all_documents
from src.embeddings import MODEL_NAME


# Minimum similarity score required for a result
MIN_SIMILARITY = 0.30


# Location where the FAISS index and metadata will be stored
VECTOR_STORE_PATH = Path("data/vector_store")

INDEX_PATH = VECTOR_STORE_PATH / "disaster_guidelines.index"

METADATA_PATH = VECTOR_STORE_PATH / "chunks.json"


def build_vector_store():
    """
    Load documents, create chunks, generate embeddings,
    and store them in a FAISS vector index.
    """

    print("Loading documents...")

    documents = load_all_documents()

    print("Creating chunks...")

    chunks = create_chunks(documents)

    print(f"Total chunks: {len(chunks)}")

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Creating embeddings...")

    embeddings = model.encode(
        [chunk["text"] for chunk in chunks],
        show_progress_bar=True
    )

    # FAISS expects float32 vectors.
    embeddings = np.asarray(embeddings).astype("float32")

    # Normalize vectors so inner product behaves like cosine similarity.
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    print(f"\nEmbedding dimension: {dimension}")

    # Create an exact inner-product FAISS index.
    index = faiss.IndexFlatIP(dimension)

    # Add all document embeddings to the index.
    index.add(embeddings)

    print(f"Vectors stored in FAISS: {index.ntotal}")

    # Create the vector store directory if it doesn't exist.
    VECTOR_STORE_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save FAISS index.
    faiss.write_index(
        index,
        str(INDEX_PATH)
    )

    # Save chunk metadata.
    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("\n------------------------------")
    print("VECTOR STORE CREATED")
    print("------------------------------")

    print(f"FAISS index: {INDEX_PATH}")

    print(f"Metadata: {METADATA_PATH}")

    return index, chunks


def load_vector_store():
    """
    Load an existing FAISS index and its metadata.
    """

    if not INDEX_PATH.exists() or not METADATA_PATH.exists():

        raise FileNotFoundError(
            "Vector store not found. "
            "Run build_vector_store() first."
        )

    # Load FAISS index.
    index = faiss.read_index(
        str(INDEX_PATH)
    )

    # Load chunk metadata.
    with open(
        METADATA_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        chunks = json.load(file)

    return index, chunks


def search(query, top_k=3):
    """
    Search the vector store for the most relevant chunks.

    Results below MIN_SIMILARITY are discarded.
    """

    # Load saved FAISS index and metadata.
    index, chunks = load_vector_store()

    # Load embedding model.
    model = SentenceTransformer(MODEL_NAME)

    # Convert user question into an embedding.
    query_embedding = model.encode(
        [query]
    )

    # Convert to float32 for FAISS.
    query_embedding = np.asarray(
        query_embedding
    ).astype("float32")

    # Normalize query vector.
    faiss.normalize_L2(
        query_embedding
    )

    # Search FAISS.
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    # Process each retrieved result.
    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        # FAISS uses -1 when there is no valid result.
        if index_position == -1:
            continue

        # Convert NumPy score to normal Python float.
        score = float(score)

        # Ignore weak/unrelated results.
        if score < MIN_SIMILARITY:
            continue

        # Get the corresponding chunk.
        result = chunks[index_position].copy()

        # Store similarity score.
        result["score"] = score

        # Add result to final list.
        results.append(result)

    return results


if __name__ == "__main__":

    # Build/rebuild the vector store.
    build_vector_store()

    print("\nTesting retrieval...")

    # Test question.
    question =  "What should I do during a hurricane?"

    results = search(
        question,
        top_k=3
    )

    print("\n------------------------------")
    print("RETRIEVAL RESULTS")
    print("------------------------------")

    if not results:

        print(
            "No relevant information found "
            "in the provided documents."
        )

    else:

        for number, result in enumerate(
            results,
            start=1
        ):

            print(f"\nResult {number}")

            print(
                f"Score: {result['score']:.4f}"
            )

            print(
                f"Source: {result['source']}"
            )

            print(
                f"Page: {result['page']}"
            )

            print(
                f"Text: {result['text'][:500]}"
            )