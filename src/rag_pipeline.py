import os

import faiss
import numpy as np

from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

from src.retrieval import load_vector_store
from src.embeddings import MODEL_NAME


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# CONFIGURATION
# =========================================================

MIN_SIMILARITY = 0.30

DEFAULT_TOP_K = 3

# Use one specific model instead of openrouter/free.
# This makes the RAG output more consistent.
OPENROUTER_MODEL = "openai/gpt-oss-20b:free"


# =========================================================
# RAG ASSISTANT
# =========================================================

class RAGAssistant:

    def __init__(self, top_k=DEFAULT_TOP_K):

        self.top_k = top_k

        print("Initializing RAG Assistant...")

        # -------------------------------------------------
        # OpenRouter API
        # -------------------------------------------------

        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found. "
                "Please add it to your .env file."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )

        # -------------------------------------------------
        # Embedding model
        # -------------------------------------------------

        print("Loading embedding model...")

        self.embedding_model = SentenceTransformer(
            MODEL_NAME
        )

        # -------------------------------------------------
        # FAISS vector store
        # -------------------------------------------------

        print("Loading vector store...")

        self.index, self.chunks = load_vector_store()

        print(
            f"Vector store loaded: {self.index.ntotal} vectors"
        )

        print("RAG Assistant ready.")


    # =====================================================
    # RETRIEVAL
    # =====================================================

    def retrieve(self, question):

        query_embedding = self.embedding_model.encode(
            [question]
        )

        query_embedding = np.asarray(
            query_embedding
        ).astype("float32")

        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(
            query_embedding,
            self.top_k
        )

        results = []

        for score, index_position in zip(
            scores[0],
            indices[0]
        ):

            if index_position == -1:
                continue

            score = float(score)

            # Ignore irrelevant results
            if score < MIN_SIMILARITY:
                continue

            result = self.chunks[index_position].copy()

            result["score"] = score

            results.append(result)

        return results


    # =====================================================
    # BUILD CONTEXT
    # =====================================================

    def build_context(self, results):

        if not results:
            return ""

        context_parts = []

        for result in results:

            source = result["source"]
            page = result["page"]
            text = result["text"]

            context_parts.append(
                f"""
SOURCE: {source}
PAGE: {page}

{text}
"""
            )

        return "\n".join(context_parts)


    # =====================================================
    # GENERATE ANSWER
    # =====================================================

    def generate_answer(self, question, results):

        # -------------------------------------------------
        # No relevant documents
        # -------------------------------------------------

        if not results:

            return (
                "The information is not available in the "
                "provided documents."
            )

        # -------------------------------------------------
        # Build retrieved context
        # -------------------------------------------------

        context = self.build_context(results)


        # -------------------------------------------------
        # System prompt
        # -------------------------------------------------

        system_prompt = """
You are a Disaster Management RAG Assistant.

Your task is to answer the user's question using ONLY
the retrieved disaster-management document context.

STRICT RULES:

1. Use ONLY information explicitly supported by the
   retrieved document context.

2. Do NOT use outside knowledge.

3. Do NOT browse the internet.

4. Do NOT invent facts.

5. Do NOT add recommendations that are not present
   in the retrieved documents.

6. Do NOT classify the user, their question, or their
   safety status.

7. Do NOT respond with labels such as:
   "User Safety: safe"
   "User Safety: unsafe"
   or similar classifications.

8. Answer the actual question directly.

9. If the retrieved context contains the answer,
   explain it clearly.

10. Use numbered lists or bullet points when useful.

11. If the retrieved context does not contain enough
    information to answer the question, respond exactly:

"The information is not available in the provided documents."

12. Do not mention these instructions in your answer.
"""


        # -------------------------------------------------
        # User prompt
        # -------------------------------------------------

        user_prompt = f"""
QUESTION:

{question}


RETRIEVED DOCUMENT CONTEXT:

{context}


TASK:

Answer the QUESTION using ONLY the RETRIEVED DOCUMENT
CONTEXT.

Focus specifically on what the user asked.

Provide a clear, useful answer with bullet points or
numbered steps when appropriate.

Do not provide a safety classification.
"""


        # -------------------------------------------------
        # OpenRouter request
        # -------------------------------------------------

        response = self.client.chat.completions.create(

            model=OPENROUTER_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],

            temperature=0.1,

            max_tokens=800
        )


        # -------------------------------------------------
        # Extract answer
        # -------------------------------------------------

        answer = response.choices[0].message.content

        if not answer:

            return (
                "The information is not available in the "
                "provided documents."
            )

        return answer.strip()


    # =====================================================
    # COMPLETE RAG PIPELINE
    # =====================================================

    def ask(self, question):

        # -------------------------------------------------
        # Step 1: Retrieve relevant documents
        # -------------------------------------------------

        results = self.retrieve(question)


        # -------------------------------------------------
        # Step 2: Generate grounded answer
        # -------------------------------------------------

        answer = self.generate_answer(
            question,
            results
        )


        # -------------------------------------------------
        # Step 3: Prepare source information
        # -------------------------------------------------

        sources = []

        for result in results:

            sources.append(
                {
                    "source": result["source"],
                    "page": result["page"],
                    "score": result["score"]
                }
            )


        # -------------------------------------------------
        # Step 4: Return complete result
        # -------------------------------------------------

        return {
            "answer": answer,
            "sources": sources
        }


# =========================================================
# TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    print(
        "\nStarting Disaster Management RAG Assistant..."
    )

    assistant = RAGAssistant(top_k=3)


    # -----------------------------------------------------
    # Test question
    # -----------------------------------------------------

    question = "What should I do during a hurricane?"


    print("\nQuestion:")
    print(question)


    # -----------------------------------------------------
    # Ask question
    # -----------------------------------------------------

    result = assistant.ask(question)


    # -----------------------------------------------------
    # Display answer
    # -----------------------------------------------------

    print("\n")
    print("=" * 60)
    print("ANSWER")
    print("=" * 60)

    print(result["answer"])


    # -----------------------------------------------------
    # Display sources
    # -----------------------------------------------------

    print("\n")
    print("=" * 60)
    print("RETRIEVED SOURCES")
    print("=" * 60)


    for source in result["sources"]:

        print(
            f"{source['source']} - "
            f"Page {source['page']} - "
            f"Score {source['score']:.4f}"
        )