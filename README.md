# 🚨 Resilience RAG Assistant

A **Retrieval-Augmented Generation (RAG)** based Disaster Management Assistant that answers questions using the provided cyclone, earthquake, and flood guideline documents.

The application retrieves relevant information from the disaster-management knowledge base using semantic similarity search and then generates an answer using an LLM through OpenRouter.

The system is designed to provide **document-grounded answers** and avoid generating unsupported information when the requested information is not available in the provided documents.

---

# 🎯 Project Objective

The objective of this project is to build a RAG-based assistant capable of answering disaster-management questions using the provided guideline documents.

The system supports:

- 🌪️ Cyclone / Hurricane guidance
- 🌎 Earthquake safety guidance
- 🌊 Flood safety guidance

The assistant retrieves relevant document sections before generating an answer and displays:

- Source document
- Page number
- Similarity score

This allows users to understand which parts of the knowledge base were retrieved for their question.

---

# 🧠 What is RAG?

**Retrieval-Augmented Generation (RAG)** combines information retrieval with language generation.

Instead of directly asking an LLM to answer a question, the system first searches the provided knowledge base for relevant information.

The retrieved information is then supplied to the LLM as context.

This helps the system generate answers that are grounded in the provided documents.

## RAG Workflow

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Retrieve Top-K Relevant Chunks
      ↓
Similarity Threshold Filtering
      ↓
Build Retrieved Context
      ↓
OpenRouter LLM
      ↓
Grounded Answer
      ↓
Source Attribution
🏗️ System Architecture
                ┌──────────────────────┐
                │   Disaster PDFs      │
                │                      │
                │ Cyclone              │
                │ Earthquake           │
                │ Flood                │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  Document Loader     │
                │       pypdf          │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    Text Chunking     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Sentence Transformer │
                │ all-MiniLM-L6-v2     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     Embeddings       │
                │    384 dimensions    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    FAISS Index       │
                │ Similarity Retrieval │
                └──────────────────────┘


User Question
      │
      ▼
Question Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Top 3 Relevant Chunks
      │
      ▼
Similarity Threshold
      │
      ▼
Retrieved Context
      │
      ▼
OpenRouter LLM
      │
      ▼
Final Answer + Sources
📚 Knowledge Base

The current knowledge base contains three disaster-management guideline documents.

🌪️ Cyclone / Hurricane

File: cyclone_guidelines.pdf

Contains information related to:

Hurricane preparedness
Safe shelter
Evacuation
Emergency communication
Severe wind safety
Floodwater safety
Emergency actions
🌎 Earthquake

File: earthquake_guidelines.pdf

Contains information related to:

Earthquake preparedness
Indoor safety
Outdoor safety
Vehicle safety
Protection from falling objects
Situations involving debris
Actions after an earthquake
🌊 Flood

File: flood_guidelines.pdf

Contains information related to:

Flood preparedness
Flood warnings
Evacuation
Floodwater safety
Emergency actions
Post-flood safety
🔧 Technologies Used
Technology	Purpose
Python	Main programming language
Streamlit	Web application and user interface
pypdf	PDF text extraction
Sentence Transformers	Text embedding generation
all-MiniLM-L6-v2	Sentence embedding model
FAISS	Vector similarity search
NumPy	Vector and numerical operations
OpenRouter	LLM API
OpenAI Python SDK	API communication
python-dotenv	Environment variable management
🔍 Implementation Details
1. Document Loading

The PDF documents are loaded and converted into text using pypdf.

Each extracted page is stored with metadata:

Source
Page
Text

The metadata is preserved throughout the pipeline so that retrieved information can later be associated with its source document and page.

✂️ 2. Text Chunking

The extracted document text is divided into smaller chunks before creating embeddings.

Chunking is important because searching entire documents as a single vector would make retrieval less precise.

Smaller chunks allow the system to retrieve specific sections that are semantically related to the user's question.

The current knowledge base contains:

13 document pages
41 text chunks

Each chunk retains:

Source
Page
Text
🧠 3. Embeddings

The project uses the Sentence Transformers model:

all-MiniLM-L6-v2

The model converts document chunks into numerical vector representations.

The generated embeddings have:

384 dimensions

The same embedding model is used for:

Document chunks
User queries

Using the same embedding space allows semantic similarity between a question and document chunks to be calculated.

🔎 4. Vector Retrieval

FAISS is used for vector similarity search.

For each user question, the application:

Converts the question into an embedding.
Converts the embedding to float32.
Normalizes the query vector.
Searches the FAISS index.
Retrieves the top 3 most similar chunks.
Applies the similarity threshold.
Uses the remaining chunks as context for the LLM.
Retrieval Configuration
Embedding Model:       all-MiniLM-L6-v2
Embedding Dimension:   384
Vector Store:           FAISS
Index Type:             IndexFlatIP
Top-K:                  3
Similarity Threshold:  0.30

The vectors are normalized before similarity search.

Because normalized vectors are searched using inner product, the resulting similarity behaves as cosine similarity.

🛡️ 5. Grounding and Hallucination Handling

A major design goal is to prevent the assistant from generating unsupported information.

The retrieval pipeline uses:

MIN_SIMILARITY = 0.30

Retrieved chunks with scores below this threshold are ignored.

If no relevant chunks remain, the application returns:

The information is not available in the provided documents.
Example Out-of-Scope Test
Question
What is the capital of France?
System Response
The information is not available in the provided documents.

This demonstrates that the system does not intentionally answer unrelated questions using outside knowledge.

The LLM prompt also instructs the model to:

Use only retrieved document context.
Avoid unsupported facts.
Avoid outside knowledge.
State when the information is unavailable.
Provide clear answers based on retrieved context.
🤖 6. Answer Generation

After retrieval, the relevant chunks are combined into a context containing:

SOURCE
PAGE
TEXT

The context is passed to the OpenRouter LLM.

The LLM is instructed to answer the user's question using only the retrieved context.

Question
   +
Retrieved Context
   ↓
OpenRouter LLM
   ↓
Grounded Answer
📖 7. Source Attribution

The application displays the retrieved sources below the generated answer.

For each retrieved result, the UI displays:

Source document
Page number
Similarity score

Example:

cyclone_guidelines.pdf
Page: 2
Similarity: 0.7357

This provides transparency about which document sections were retrieved for the answer.

🖥️ User Interface

The application is implemented using Streamlit.

The interface contains:

Disaster category information cards
Question input
Ask Question button
Generated answer
Retrieved sources
Similarity scores
System architecture information
Knowledge-base information
Safety disclaimer
📊 Evaluation

The system was tested using questions from all supported disaster categories and an out-of-scope question.

Supported Tests
Hurricane
What should I do during a hurricane?

Expected behavior:

Retrieve cyclone/hurricane information.
Generate an answer grounded in the retrieved document.
Display the source and similarity score.
Earthquake
What should I do during an earthquake?

Expected behavior:

Retrieve earthquake-related information.
Generate a document-grounded answer.
Display the source and similarity score.
Flood
What should I do when there is a flood warning?

Expected behavior:

Retrieve flood-related information.
Generate a document-grounded answer.
Display the source and similarity score.
Out-of-Scope
What is the capital of France?

Expected behavior:

The information is not available in the provided documents.
🧪 10 Sample Question-and-Answer Evaluation

The project includes an evaluation file:

evaluation/sample_questions.json

The evaluation set is intended to contain 10 sample question-and-answer outputs covering:

Hurricane-related questions
Earthquake-related questions
Flood-related questions
Out-of-scope questions

The evaluation focuses on:

Retrieval relevance
Answer grounding
Source attribution
Out-of-scope handling
Similarity scores

Example evaluation structure:

Question
    ↓
Retrieved Source
    ↓
Page
    ↓
Similarity Score
    ↓
Generated Answer
    ↓
Grounding Check
🎯 Evaluation Criteria

The following criteria are used to evaluate the RAG system:

Criterion	Description
Retrieval Relevance	Retrieved chunks should be related to the question
Grounded Answer	Answer should be supported by retrieved context
Source Attribution	Source document and page should be displayed
Out-of-Scope Handling	Unsupported questions should not receive fabricated answers
Response Quality	Answers should be clear and practically useful
System Reliability	Pipeline should consistently load, retrieve and generate responses
📸 Screenshots
🌪️ Hurricane / Cyclone

The assistant retrieves relevant hurricane guidance and displays the source document and similarity score.

🌎 Earthquake

The assistant retrieves earthquake-related safety guidance from the earthquake document.

🌊 Flood

The assistant retrieves relevant flood-management information.

❌ Out-of-Scope Question

The assistant avoids generating an unsupported answer when relevant information cannot be found in the knowledge base.

🧩 Challenges and Design Decisions
Why use RAG?

A standard LLM may generate information from its general pretrained knowledge.

For this project, the goal is to answer using the provided disaster-management documents.

RAG provides a mechanism to retrieve relevant document information before generating an answer.

Why use Sentence Transformers?

Sentence Transformers provide semantic embeddings that allow questions and document chunks to be compared based on meaning rather than only exact keyword matching.

Why use FAISS?

FAISS provides efficient similarity search over numerical embeddings and is suitable for building a lightweight local vector store.

Why use Top-K = 3?

The system retrieves the three highest-scoring chunks to provide enough context while keeping the context focused.

Why use a similarity threshold?

The threshold helps prevent weakly related chunks from being passed to the LLM.

The current threshold is:

0.30
Why use source attribution?

Displaying the source document, page and similarity score makes the retrieval process more transparent and allows the generated response to be traced back to the knowledge base.

📁 Project Structure
RESILIENCE-RAG-ASSISTANT/
│
├── data/
│   ├── documents/
│   │   ├── cyclone_guidelines.pdf
│   │   ├── earthquake_guidelines.pdf
│   │   └── flood_guidelines.pdf
│   │
│   └── vector_store/
│       ├── chunks.json
│       └── disaster_guidelines.index
│
├── evaluation/
│   └── sample_questions.json
│
├── screenshots/
│   ├── hurricane.png
│   ├── earthquake.png
│   ├── flood.png
│   └── out_of_scope.png
│
├── src/
│   ├── __init__.py
│   ├── chunking.py
│   ├── document_loader.py
│   ├── embeddings.py
│   ├── openrouter_test.py
│   ├── rag_pipeline.py
│   └── retrieval.py
│
├── .gitignore
├── app.py
├── README.md
├── requirements.txt
└── PROJECT_SUMMARY.md

PROJECT_SUMMARY.md should be added to the repository when the one-page project summary is created.

🚀 Installation
1. Clone the Repository
git clone https://github.com/Nitheeshhd/resilience-rag-assistant.git
cd resilience-rag-assistant
2. Create a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Verify Dependencies
pip check

Expected result:

No broken requirements found.
🔑 Environment Configuration

Create a .env file in the project root:

OPENROUTER_API_KEY=your_openrouter_api_key

Replace the placeholder with your own OpenRouter API key.

Security

The .env file is intentionally excluded from Git using .gitignore.

The API key must never be committed or publicly exposed.

▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

The application will open in the browser.

⚙️ Rebuild the Vector Store

The vector store can be rebuilt from the source documents using:

python src/retrieval.py

This process:

Loads the documents.
Creates text chunks.
Generates embeddings.
Builds the FAISS index.
Stores chunk metadata.

The generated vector-store files are:

data/vector_store/disaster_guidelines.index
data/vector_store/chunks.json
🧩 Main Components
document_loader.py

Loads and extracts text from the PDF documents.

chunking.py

Splits extracted document content into smaller searchable chunks.

embeddings.py

Creates Sentence Transformer embeddings using:

all-MiniLM-L6-v2
retrieval.py

Builds and searches the FAISS vector store.

rag_pipeline.py

Combines:

Retrieval
Context construction
OpenRouter generation
Source attribution
app.py

Provides the Streamlit user interface.

📚 Research References

The implementation is based on established research in Retrieval-Augmented Generation, sentence embeddings and vector similarity search.

Retrieval-Augmented Generation

Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks."

This work introduced the approach of combining retrieved external knowledge with language generation.

Sentence-BERT

Reimers and Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks."

This work provides the foundation for generating semantically meaningful sentence embeddings, which are used in this project through Sentence Transformers.

FAISS

Johnson, Douze and Jégou, "Billion-scale similarity search with GPUs."

This work describes efficient similarity search approaches for high-dimensional vector representations.

⚠️ Safety Disclaimer

This application is an information-retrieval and demonstration system based on the provided disaster-management documents.

It should not replace instructions from local emergency authorities during an actual disaster.

During an actual emergency, users should follow official warnings and instructions from the appropriate emergency authorities.

🔮 Future Improvements

Possible improvements include:

Expanding the disaster-document knowledge base
Adding comprehensive evaluation datasets
Adding automatic evaluation metrics
Hybrid keyword and semantic retrieval
Reranking retrieved chunks
Multilingual disaster guidance
Conversation history
Document upload through the UI
Streaming LLM responses
Automated hallucination evaluation
Improved source highlighting
👨‍💻 Author

Nitheesh H D

Developed as an AI/ML internship project demonstrating Retrieval-Augmented Generation for disaster-management information retrieval and question answering.

📌 GitHub Repository

Resilience RAG Assistant

Repository:

https://github.com/Nitheeshhd/resilience-rag-assistant
