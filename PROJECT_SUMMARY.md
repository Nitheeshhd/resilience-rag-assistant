# Project Summary - Resilience RAG Assistant

## 1. Project Overview

The Resilience RAG Assistant is a Retrieval-Augmented Generation (RAG) application designed to answer disaster-management questions using the provided cyclone, earthquake, and flood guideline documents.

The objective is to retrieve relevant information from the document collection and use the retrieved content as context for generating grounded answers. The application also displays the source document, page number, and similarity score for retrieved information.

The application is implemented using Python and Streamlit.

---

## 2. Approach

The system follows a complete RAG pipeline:

```text
Disaster PDF Documents
        |
        v
Document Loading
        |
        v
Text Chunking
        |
        v
Sentence Embeddings
        |
        v
FAISS Vector Store
        |
        v
User Question Embedding
        |
        v
Similarity Search
        |
        v
Top-K Relevant Chunks
        |
        v
Similarity Threshold Filtering
        |
        v
Retrieved Context
        |
        v
OpenRouter LLM
        |
        v
Grounded Answer + Sources

The three provided disaster-management documents are first loaded and converted into text. The extracted content is divided into smaller chunks so that relevant sections can be retrieved more precisely.

The chunks are converted into vector representations using the all-MiniLM-L6-v2 Sentence Transformer model. These vectors are stored in a FAISS index.

When a user asks a question, the same embedding model converts the question into a vector. FAISS then retrieves the most similar document chunks.

The retrieved chunks are passed as context to an OpenRouter-hosted LLM, which generates the final answer using only the retrieved information.

3. Technical Decisions
Document Processing

pypdf is used to extract text from the provided PDF documents.

The document collection contains:

Cyclone / Hurricane guidelines
Earthquake guidelines
Flood guidelines

The current collection contains 13 document pages and produces 41 searchable text chunks.

Chunking

The documents are divided into smaller text chunks before embedding.

Chunking improves retrieval precision because the system can retrieve relevant sections instead of treating an entire document as a single vector.

Each chunk retains its source document and page metadata.

Embedding Model

The project uses:

all-MiniLM-L6-v2

The model converts text into 384-dimensional embeddings.

The same model is used for both document chunks and user queries so that they can be compared in the same vector space.

Vector Database

FAISS is used for similarity search.

The implementation uses normalized embeddings and an IndexFlatIP index. With normalized vectors, inner-product similarity behaves as cosine similarity.

The system retrieves the top 3 most relevant chunks for each question.

Similarity Threshold

A minimum similarity threshold of:

0.30

is used to filter weakly related retrieval results.

This helps prevent irrelevant document chunks from being passed to the language model.

Language Model

OpenRouter is used to access the language model.

The LLM receives the user's question together with the retrieved document context.

The prompt instructs the model to answer only from the retrieved documents and to avoid using outside knowledge.

4. Grounding and Hallucination Handling

The system is designed to reduce unsupported answers.

If no retrieved chunk meets the configured similarity threshold, the system returns:

The information is not available in the provided documents.

An out-of-scope test was performed using:

What is the capital of France?

The system correctly returned that the information was not available in the provided documents instead of providing an unrelated answer.

The LLM prompt also explicitly instructs the model to:

Use only the retrieved context.
Avoid inventing facts.
Avoid outside knowledge.
State when information is unavailable.
Provide answers grounded in the supplied documents.
5. User Interface

The application uses Streamlit to provide a simple web interface.

The interface includes:

Disaster category information cards
Question input
Ask Question button
Generated answer
Retrieved source documents
Page numbers
Similarity scores
System architecture information
Knowledge-base information
Safety disclaimer

This allows users to interact with the RAG system without directly using the command line.

6. Evaluation

The RAG pipeline was tested using questions covering:

Cyclone / Hurricane
Earthquake
Flood
Out-of-scope questions

A 10-question evaluation script was created to run the questions automatically and save the generated results to:

evaluation/evaluation_results.json

The evaluation records the question, category, generated answer, retrieved sources, page numbers, and similarity scores.

The evaluation also includes an out-of-scope question to verify that the system does not intentionally answer questions that are unrelated to the provided disaster-management documents.

7. Challenges
API Rate Limiting

During evaluation, the OpenRouter free provider temporarily returned a 429 rate-limit response for one request.

This was an upstream provider limitation rather than a failure of the document retrieval or FAISS components.

Out-of-Scope Retrieval

Semantic retrieval can sometimes return moderately similar chunks even when the exact answer is not present in the documents.

To address this, a similarity threshold is used before sending retrieved content to the language model.

Grounded Generation

The language model could potentially generate information beyond the retrieved context.

To reduce this risk, the system prompt explicitly restricts the model to the retrieved disaster-management documents.

8. Results

The complete RAG pipeline successfully performs:

PDF Loading
      |
      v
Text Chunking
      |
      v
Embedding Generation
      |
      v
FAISS Indexing
      |
      v
Semantic Retrieval
      |
      v
Context Construction
      |
      v
LLM Generation
      |
      v
Source Attribution

The system successfully retrieves relevant cyclone, earthquake, and flood information for supported questions.

For unrelated questions, the similarity threshold and grounding instructions allow the system to return an unavailable-information response instead of intentionally using outside knowledge.

The Streamlit interface provides a user-friendly way to interact with the complete pipeline.

9. Future Improvements

Possible improvements include:

Expanding the disaster-management document collection.
Adding a larger automated evaluation dataset.
Adding automated answer-grounding metrics.
Adding hybrid keyword and semantic retrieval.
Adding a reranking stage for retrieved chunks.
Supporting multiple languages.
Adding document upload through the Streamlit interface.
Adding conversation history.
Improving source highlighting.
Adding retry handling for temporary LLM API rate limits.
10. Conclusion

The Resilience RAG Assistant demonstrates how Retrieval-Augmented Generation can be used to build a document-grounded disaster-management question-answering system.

The project combines document processing, semantic embeddings, FAISS similarity search, similarity filtering, LLM-based generation, source attribution, and a Streamlit interface into a complete end-to-end application.

The implementation focuses on keeping generated answers grounded in the provided disaster-management documents while providing transparency through retrieved sources and similarity scores.
