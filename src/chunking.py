from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.document_loader import load_all_documents


CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def create_chunks(documents):
    """
    Split extracted documents into smaller chunks while
    preserving source and page metadata.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = []

    for document in documents:

        text_chunks = splitter.split_text(document["text"])

        for chunk in text_chunks:

            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "page": document["page"],
                }
            )

    return chunks


if __name__ == "__main__":

    documents = load_all_documents()

    chunks = create_chunks(documents)

    print("\n------------------------------")
    print("CHUNKING COMPLETE")
    print("------------------------------")

    print(f"Original pages: {len(documents)}")
    print(f"Total chunks: {len(chunks)}")

    if chunks:

        print("\nFirst chunk:")
        print("------------------------------")
        print(chunks[0]["text"])

        print("\nMetadata:")
        print(f"Source: {chunks[0]['source']}")
        print(f"Page: {chunks[0]['page']}")

        print("\nChunk length:")
        print(len(chunks[0]["text"]))