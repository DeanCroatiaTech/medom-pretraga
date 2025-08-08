from typing import Set

from backend.core import run_llm
import streamlit as st

# Set page config
st.set_page_config(
    page_title="MeDom Nekretnine Asistent",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for black and white minimalist design
st.markdown("""
<style>
/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Global styles */
.stApp {
    background: #ffffff;
    min-height: 100vh;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Main container */
.main-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px 40px 20px;
    background: #ffffff;
    margin-bottom: 120px;
    margin-top: 0;
}

/* Header styling */
.header-container {
    text-align: center;
    padding: 20px 0;
    border-bottom: 1px solid #e5e5e5;
    margin-bottom: 30px;
    background: #ffffff;
    position: sticky;
    top: 0;
    z-index: 100;
    margin-top: 0;
}

.header-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #000000;
    margin-bottom: 10px;
    letter-spacing: -0.02em;
}

.header-subtitle {
    font-size: 1.1rem;
    color: #666666;
    font-weight: 400;
}

/* Chat messages styling */
.chat-container {
    padding: 20px 0;
}

.user-message {
    background: #000000;
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 12px 12px 4px 12px;
    margin: 16px 0;
    max-width: 80%;
    margin-left: auto;
    font-size: 15px;
    line-height: 1.5;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.assistant-message {
    background: #f8f9fa;
    color: #000000;
    padding: 16px 20px;
    border-radius: 12px 12px 12px 4px;
    margin: 16px 0;
    max-width: 80%;
    border: 1px solid #e5e5e5;
    font-size: 15px;
    line-height: 1.5;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

/* Floating input styling */
.floating-input {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #ffffff;
    padding: 20px;
    border-top: 1px solid #e5e5e5;
    z-index: 1000;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1);
}

.input-container {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
}

.stTextInput > div > div > input {
    border-radius: 12px;
    border: 2px solid #e5e5e5;
    padding: 16px 24px;
    font-size: 16px;
    transition: all 0.2s ease;
    background: #ffffff;
    color: #000000;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stTextInput > div > div > input:focus {
    border-color: #000000;
    box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
    outline: none;
}

.stTextInput > div > div > input::placeholder {
    color: #999999;
}

/* Spinner styling */
.stSpinner > div {
    border-color: #000000 !important;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-container {
        margin: 10px;
        padding: 20px 15px;
    }

    .header-title {
        font-size: 2rem;
    }

    .user-message, .assistant-message {
        max-width: 90%;
        font-size: 14px;
    }

    .floating-input {
        padding: 15px;
    }

    .stTextInput > div > div > input {
        padding: 14px 20px;
        font-size: 15px;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if (
        "chat_answers_history" not in st.session_state
        and "user_prompt_history" not in st.session_state
        and "chat_history" not in st.session_state
):
    st.session_state["chat_answers_history"] = []
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_history"] = []

# Initialize input clearing flag
if "clear_input" not in st.session_state:
    st.session_state["clear_input"] = False


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "**Izvori:**\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


def create_individual_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "\n\n**Izvori:**\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="header-title">MeDom Nekretnine</div>
    <div class="header-subtitle">Vaš AI-asistent za nekretnine</div>
</div>
""", unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
            st.session_state["chat_answers_history"],
            st.session_state["user_prompt_history"],
    ):
        # User message
        st.markdown(f'<div class="user-message">{user_query}</div>', unsafe_allow_html=True)

        # Assistant message
        st.markdown(f'<div class="assistant-message">{generated_response}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Floating input at bottom
st.markdown('<div class="floating-input">', unsafe_allow_html=True)
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Use a unique key that changes when we want to clear the input
input_key = f"floating_prompt_{st.session_state.get('input_counter', 0)}"
prompt = st.text_input("", placeholder="Traži...", key=input_key, label_visibility="collapsed")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Handle prompt submission
if prompt and not st.session_state.get("clear_input", False):
    with st.spinner("Razmišljam..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']}{create_individual_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

    # Clear the input by incrementing the counter
    st.session_state["input_counter"] = st.session_state.get("input_counter", 0) + 1
    st.session_state["clear_input"] = True
    st.rerun()

# Reset the clear flag after processing
if st.session_state.get("clear_input", False):
    st.session_state["clear_input"] = False