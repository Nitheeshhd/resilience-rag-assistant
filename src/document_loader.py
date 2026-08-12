from pathlib import Path
from pypdf import PdfReader


DOCUMENTS_PATH = Path("data/documents")


def load_pdf(file_path):
    """
    Load a single PDF and extract text page by page.

    Returns:
        list: A list of dictionaries containing:
              - text
              - source
              - page
    """

    reader = PdfReader(file_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            documents.append(
                {
                    "text": text.strip(),
                    "source": file_path.name,
                    "page": page_number,
                }
            )

    return documents


def load_all_documents():
    """
    Load all PDF documents from the documents folder.
    """

    all_documents = []

    pdf_files = sorted(DOCUMENTS_PATH.glob("*.pdf"))

    for pdf_file in pdf_files:
        print(f"Loading: {pdf_file.name}")

        documents = load_pdf(pdf_file)

        print(f"  Pages with text: {len(documents)}")

        all_documents.extend(documents)

    return all_documents


if __name__ == "__main__":
    documents = load_all_documents()

    print("\n------------------------------")
    print("DOCUMENT LOADING COMPLETE")
    print("------------------------------")

    print(f"Total pages loaded: {len(documents)}")

    if documents:
        print("\nFirst document:")
        print(f"Source: {documents[0]['source']}")
        print(f"Page: {documents[0]['page']}")
        print(f"\nText preview:\n{documents[0]['text'][:500]}")