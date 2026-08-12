from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


def create_embedding_model():
    """
    Load the sentence-transformer embedding model.
    """

    model = SentenceTransformer(MODEL_NAME)

    return model


def create_embeddings(chunks, model):
    """
    Generate embeddings for all text chunks.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings


if __name__ == "__main__":

    from src.chunking import create_chunks
    from src.document_loader import load_all_documents

    print("Loading documents...")

    documents = load_all_documents()

    print("Creating chunks...")

    chunks = create_chunks(documents)

    print(f"Total chunks: {len(chunks)}")

    print("\nLoading embedding model...")

    model = create_embedding_model()

    print("Creating embeddings...")

    embeddings = create_embeddings(chunks, model)

    print("\n------------------------------")
    print("EMBEDDING CREATION COMPLETE")
    print("------------------------------")

    print(f"Number of chunks: {len(chunks)}")
    print(f"Embedding shape: {embeddings.shape}")

    print("\nFirst embedding:")
    print(embeddings[0])