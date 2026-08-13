# Resilience RAG Assistant

A document-grounded disaster-management question-answering application built using **Retrieval-Augmented Generation (RAG)**.

The application retrieves relevant information from provided **Cyclone/Hurricane, Earthquake, and Flood guideline documents** and uses the retrieved content as context for generating answers through an OpenRouter-hosted LLM.

The system also displays the retrieved source document, page number, and similarity score to provide transparency about where the answer comes from.

---

## Project Overview

The **Resilience RAG Assistant** is designed to answer disaster-preparedness questions using only the information available in the provided disaster-management documents.

Instead of directly asking a language model to answer a question, the system first searches the document knowledge base for relevant information.

The retrieved information is then provided to the language model as context.

### Core workflow

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
User Question
        |
        v
Question Embedding
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
Grounded Answer
        |
        v
Source Attribution
Key Features
Document-grounded disaster-management question answering
Cyclone / Hurricane guidance
Earthquake safety guidance
Flood safety guidance
PDF text extraction using pypdf
Text chunking for improved retrieval
Semantic embeddings using all-MiniLM-L6-v2
FAISS vector similarity search
Cosine-similarity-based retrieval
Top-3 relevant chunk retrieval
Similarity threshold filtering
OpenRouter LLM integration
Source document attribution
Page number display
Similarity score display
Out-of-scope question handling
Streamlit web interface
Automated evaluation script
Evaluation result storage in JSON format
Knowledge Base

The current knowledge base contains three disaster-management guideline documents:

data/documents/

├── cyclone_guidelines.pdf
├── earthquake_guidelines.pdf
└── flood_guidelines.pdf

The current document collection contains:

13 document pages
41 searchable text chunks

The chunks retain metadata such as:

Source document
Page number
Extracted text
Technologies Used
Technology	Purpose
Python	Core application development
Streamlit	Web-based user interface
pypdf	PDF text extraction
Sentence Transformers	Text embedding generation
all-MiniLM-L6-v2	Sentence embedding model
FAISS	Vector similarity search
NumPy	Numerical and embedding operations
OpenAI Python SDK	API client for OpenRouter
OpenRouter	LLM access
python-dotenv	Environment variable management
JSON	Metadata and evaluation result storage
Why These Technologies Are Used
Python

Python is used as the main programming language because it provides libraries for document processing, embeddings, vector search, API integration, and application development.

Streamlit

Streamlit provides a simple interactive web interface for users to ask disaster-management questions without directly interacting with the command line.

pypdf

pypdf is used to extract text from the provided PDF documents page by page.

Each extracted page is stored together with its source filename and page number.

Sentence Transformers

Sentence Transformers are used to convert document chunks and user questions into numerical vector representations.

The project uses:

all-MiniLM-L6-v2

The model generates 384-dimensional embeddings.

FAISS

FAISS is used as the vector search engine.

The project uses:

IndexFlatIP

The embeddings are normalized before indexing.

Because the vectors are normalized, inner-product similarity behaves as cosine similarity.

OpenRouter

OpenRouter is used to provide access to the language model.

The retrieved document context is sent to the LLM together with the user's question.

python-dotenv

python-dotenv loads the OpenRouter API key from the local .env file.

The .env file is excluded from Git using .gitignore.

RAG Pipeline
1. Document Loading

The system loads all PDF files from:

data/documents/

Each page containing text is converted into a document record containing:

text
source
page
2. Text Chunking

The extracted document text is divided into smaller chunks.

Chunking allows the system to retrieve specific relevant sections rather than searching an entire document as one large unit.

Each chunk maintains its source and page metadata.

3. Embedding Generation

Each text chunk is converted into a vector using:

all-MiniLM-L6-v2

The same embedding model is used for user questions.

This allows document chunks and questions to be compared in the same vector space.

4. FAISS Indexing

The generated embeddings are normalized and stored in a FAISS index.

The current vector store contains:

41 vectors

with an embedding dimension of:

384

The vector store is stored in:

data/vector_store/

with:

disaster_guidelines.index
chunks.json
5. Question Retrieval

When the user asks a question:

The question is converted into an embedding.
The query embedding is normalized.
FAISS searches for the most similar document chunks.
The top 3 results are retrieved.
Results below the similarity threshold are removed.

The configured similarity threshold is:

0.30
6. Context Construction

The relevant retrieved chunks are combined into a context containing:

Source document
Page number
Retrieved text

This context is then passed to the language model.

7. Grounded Generation

The LLM receives:

The user's question
Retrieved document context
Grounding instructions

The system prompt instructs the LLM to:

Use only the retrieved context.
Avoid inventing facts.
Avoid outside knowledge.
Answer only from the provided documents.
State when the required information is unavailable.
Out-of-Scope Handling

The system is designed to avoid intentionally answering questions that are unrelated to the knowledge base.

For example:

What is the capital of France?

If no relevant document information passes the similarity threshold, the system returns:

The information is not available in the provided documents.

This helps reduce unsupported answers and keeps the system focused on the provided disaster-management documents.

User Interface

The application is built using Streamlit.

The interface provides:

Disaster Information Cards

The UI displays information cards for:

Cyclone / Hurricane
Earthquake
Flood
Question Input

Users can enter a disaster-management question through the text input area.

Example:

What should I do during a hurricane?
Generated Answer

The system displays the answer generated using the retrieved document context.

Retrieved Sources

For each retrieved source, the application displays:

Source document
Page number
Similarity score

Example:

cyclone_guidelines.pdf
Page: 2
Similarity: 0.7357
Safety Disclaimer

The application includes a disclaimer explaining that it is an information and demonstration tool and should not replace instructions from local emergency authorities during an actual disaster.

Project Structure
resilience-rag-assistant/
|
├── data/
│   ├── documents/
│   │   ├── cyclone_guidelines.pdf
│   │   ├── earthquake_guidelines.pdf
│   │   └── flood_guidelines.pdf
│   │
│   └── vector_store/
│       ├── chunks.json
│       └── disaster_guidelines.index
|
├── evaluation/
│   ├── sample_questions.json
│   ├── run_evaluation.py
│   └── evaluation_results.json
|
├── screenshots/
│   ├── hurricane.png
│   ├── earthquake.png
│   ├── flood.png
│   └── out_of_scope.png
|
├── src/
│   ├── __init__.py
│   ├── chunking.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── openrouter_test.py
│   ├── rag_pipeline.py
│   └── retrieval.py
|
├── .gitignore
├── README.md
├── PROJECT_SUMMARY.md
├── app.py
└── requirements.txt
Installation
1. Clone the Repository
git clone https://github.com/Nitheeshhd/resilience-rag-assistant.git
cd resilience-rag-assistant
2. Create a Virtual Environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Verify Dependencies
pip check

The expected output is:

No broken requirements found.
Environment Variables

Create a .env file in the project root:

OPENROUTER_API_KEY=your_openrouter_api_key

The .env file is intentionally excluded from Git using .gitignore.

Never commit or publicly expose your API key.

Running the Application

After activating the virtual environment and configuring the API key:

streamlit run app.py

Streamlit will start the local web application.

Open the local URL displayed in the terminal.

Rebuilding the Vector Store

If the source documents are changed or new documents are added, rebuild the vector store using:

python src/retrieval.py

This process:

Loads the PDF documents.
Creates text chunks.
Generates embeddings.
Normalizes embeddings.
Creates the FAISS index.
Saves the index and chunk metadata.

The generated files are:

data/vector_store/disaster_guidelines.index
data/vector_store/chunks.json
Testing Retrieval

The retrieval module can also be executed directly:

python src/retrieval.py

The script performs a test retrieval using:

What should I do during a hurricane?

It displays:

Retrieved result number
Similarity score
Source document
Page number
Retrieved text
Evaluation

The project includes an automated evaluation script:

evaluation/run_evaluation.py

The evaluation contains 10 questions covering:

Cyclone / Hurricane
Earthquake
Flood
Out-of-scope questions

Run the evaluation from the project root:

python -m evaluation.run_evaluation

The results are saved to:

evaluation/evaluation_results.json

The evaluation results contain:

Question ID
Category
Question
Generated answer
Retrieved sources
Page numbers
Similarity scores
Errors, if any

The evaluation is intended to verify both supported disaster-management questions and out-of-scope behavior.

Evaluation Example

Example supported question:

What should I do during a hurricane?

The system retrieves relevant cyclone guidance and passes the retrieved content to the LLM.

Example out-of-scope question:

What is the capital of France?

The system should return:

The information is not available in the provided documents.
Screenshots
Hurricane / Cyclone Question

Earthquake Question

Flood Question

Out-of-Scope Question

Grounding and Safety

This project is designed to keep answers grounded in the provided disaster-management documents.

The system uses several mechanisms to reduce unsupported responses:

Similarity Threshold

Retrieved chunks with similarity scores below:

0.30

are excluded from the generation context.

Restricted LLM Prompt

The LLM is instructed to use only the retrieved document context.

Source Attribution

The UI displays the source document, page number, and similarity score for retrieved content.

Safety Disclaimer

The application is intended as an information and demonstration tool.

During an actual disaster, users should follow instructions from local emergency authorities and official emergency services.

Challenges
API Rate Limiting

During evaluation, the OpenRouter free provider temporarily returned a 429 rate-limit response for one request.

This represents an upstream provider limitation rather than a failure of the document loading, embedding, or FAISS retrieval components.

Out-of-Scope Retrieval

Semantic retrieval may sometimes identify moderately similar text even when the exact answer is not present in the documents.

The similarity threshold helps reduce the likelihood of unrelated content being passed to the LLM.

Grounded Generation

A language model can potentially generate information beyond the retrieved context.

The system prompt therefore explicitly restricts generation to the retrieved disaster-management documents.

Project Documentation

A detailed technical project summary is available in:

PROJECT_SUMMARY.md

It explains:

Project approach
RAG architecture
Technical decisions
Embedding model
FAISS implementation
Similarity threshold
Grounding strategy
Streamlit interface
Evaluation
Challenges
Results
Future improvements
Future Improvements

Possible future improvements include:

Expanding the disaster-management document collection.
Adding a larger evaluation dataset.
Adding automated answer-grounding metrics.
Adding hybrid keyword and semantic retrieval.
Adding a reranking stage.
Supporting multiple languages.
Adding document upload through the Streamlit interface.
Adding conversation history.
Improving source highlighting.
Adding retry handling for temporary LLM API rate limits.
Conclusion

The Resilience RAG Assistant demonstrates an end-to-end Retrieval-Augmented Generation system for disaster-management question answering.

The project combines:

PDF Processing
      ↓
Text Chunking
      ↓
Sentence Embeddings
      ↓
FAISS Vector Search
      ↓
Similarity Filtering
      ↓
Context Construction
      ↓
LLM Generation
      ↓
Source Attribution
      ↓
Streamlit Interface

The system focuses on producing answers grounded in the provided cyclone, earthquake, and flood guideline documents while providing source transparency through document names, page numbers, and similarity scores.

Author

Nitheesh H D

GitHub:

https://github.com/Nitheeshhd/resilience-rag-assistant