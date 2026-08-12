import streamlit as st

from src.rag_pipeline import RAGAssistant


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Disaster Management RAG Assistant",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main application */
    .main {
        padding-top: 1.5rem;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #aab2c0;
        margin-bottom: 25px;
    }

    /* Disaster cards */
    .disaster-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #333842;
        background: #17191f;
        min-height: 125px;
    }

    .disaster-title {
        font-size: 20px;
        font-weight: 650;
        margin-bottom: 8px;
    }

    .disaster-text {
        color: #aeb5c2;
        font-size: 14px;
        line-height: 1.5;
    }

    /* Answer box */
    .answer-header {
        font-size: 26px;
        font-weight: 650;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    /* Score */
    .score {
        color: #6ee7b7;
        font-weight: 600;
    }

    /* Disclaimer */
    .disclaimer {
        padding: 14px 16px;
        border-radius: 10px;
        background: #1d2430;
        border: 1px solid #303b4d;
        color: #b9c4d4;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 25px;
    }

    /* Sidebar */
    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
    }

    .architecture-item {
        padding: 7px 0;
        color: #c5cbd5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🚨 Disaster Management RAG Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    Ask disaster-preparedness questions and receive answers grounded
    in the provided disaster-management documents.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DISASTER INFORMATION CARDS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        """
        <div class="disaster-card">
            <div class="disaster-title">🌪️ Hurricane</div>
            <div class="disaster-text">
                Safety actions, shelter guidance, evacuation,
                communication and emergency preparedness.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """
        <div class="disaster-card">
            <div class="disaster-title">🌎 Earthquake</div>
            <div class="disaster-text">
                Guidance for staying safe indoors, outdoors,
                during shaking and after an earthquake.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        """
        <div class="disaster-card">
            <div class="disaster-title">🌊 Flood</div>
            <div class="disaster-text">
                Flood warnings, evacuation, floodwater safety
                and preparation guidance.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# LOAD RAG ASSISTANT
# =========================================================

@st.cache_resource
def load_assistant():

    return RAGAssistant(top_k=3)


try:

    assistant = load_assistant()

except Exception as error:

    st.error(
        "Unable to initialize the Disaster Management Assistant."
    )

    st.exception(error)

    st.stop()


# =========================================================
# QUESTION INPUT
# =========================================================

st.subheader("💬 Ask a question")


question = st.text_area(
    "Question",
    placeholder=(
        "Example: What should I do during a hurricane?"
    ),
    height=120,
    label_visibility="collapsed"
)


# =========================================================
# ASK BUTTON
# =========================================================

ask_button = st.button(
    "🔍 Ask Question",
    type="primary",
    use_container_width=False
)


if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question before clicking Ask Question."
        )

    else:

        with st.spinner(
            "Searching the disaster-management knowledge base..."
        ):

            try:

                result = assistant.ask(
                    question.strip()
                )

            except Exception as error:

                st.error(
                    "Something went wrong while processing your question."
                )

                st.exception(error)

                st.stop()


        # =================================================
        # ANSWER
        # =================================================

        st.markdown(
            '<div class="answer-header">💡 Answer</div>',
            unsafe_allow_html=True
        )

        # Markdown rendering gives us proper numbered lists
        # and bullet points.

        st.markdown(
            result["answer"]
        )


        # =================================================
        # SOURCES
        # =================================================

        st.markdown(
            '<div class="answer-header">📚 Sources</div>',
            unsafe_allow_html=True
        )


        if result["sources"]:

            for number, source in enumerate(
                result["sources"],
                start=1
            ):

                source_name = source["source"]

                page = source["page"]

                score = source["score"]


                # -----------------------------------------
                # Native Streamlit source card
                # -----------------------------------------

                with st.container(border=True):

                    st.markdown(
                        f"### 📄 {number}. {source_name}"
                    )

                    col_source_1, col_source_2 = st.columns(2)


                    with col_source_1:

                        st.write(
                            f"**Page:** {page}"
                        )


                    with col_source_2:

                        st.write(
                            f"**Similarity:** `{score:.4f}`"
                        )


        else:

            st.info(
                "No relevant source was found in the provided documents."
            )


# =========================================================
# SAFETY DISCLAIMER
# =========================================================

st.markdown(
    """
    <div class="disclaimer">

    ⚠️ <b>Important:</b>
    This assistant answers questions using only the disaster-management
    documents provided as its knowledge base. It is intended as an
    information and demonstration tool and should not replace
    instructions from local emergency authorities during an actual
    disaster.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🧠 About the System</div>',
        unsafe_allow_html=True
    )


    st.write(
        """
        This application uses Retrieval-Augmented Generation (RAG)
        to retrieve relevant information from disaster-management
        documents before generating an answer.
        """
    )


    st.markdown("---")


    # =====================================================
    # KNOWLEDGE BASE
    # =====================================================

    st.markdown("### 📚 Knowledge Base")


    st.markdown(
        """
        <div class="architecture-item">
        🌪️ Hurricane / Cyclone
        </div>

        <div class="architecture-item">
        🌎 Earthquake
        </div>

        <div class="architecture-item">
        🌊 Flood
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    # =====================================================
    # ARCHITECTURE
    # =====================================================

    st.markdown("### ⚙️ Architecture")


    st.markdown(
        """
        <div class="architecture-item">
        📄 PDF Documents
        </div>

        <div class="architecture-item">
        ✂️ Text Chunking
        </div>

        <div class="architecture-item">
        🧠 Sentence Embeddings
        </div>

        <div class="architecture-item">
        🔎 FAISS Similarity Search
        </div>

        <div class="architecture-item">
        🤖 OpenRouter LLM
        </div>

        <div class="architecture-item">
        🛡️ Relevance Threshold: 0.30
        </div>

        <div class="architecture-item">
        🔗 Source Attribution
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("---")


    # =====================================================
    # TECHNOLOGIES
    # =====================================================

    st.markdown("### 🔧 Technologies")


    st.write(
        """
        **Python**

        **Streamlit**

        **FAISS**

        **Sentence Transformers**

        **OpenRouter**
        """
    )