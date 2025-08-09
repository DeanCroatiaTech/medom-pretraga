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

# Initialize language in session state
if "lang" not in st.session_state:
    st.session_state["lang"] = "hr"  # 'hr' or 'en'

# Simple translation dictionary for UI strings
TRANSLATIONS = {
    "hr": {
        "subtitle": "Vaš AI-asistent za nekretnine",
        "search_placeholder": "Traži...",
        "send": "Pošalji",
        "thinking": "Razmišljam...",
        "sources": "Izvori",
    },
    "en": {
        "subtitle": "Your AI real estate assistant",
        "search_placeholder": "Search...",
        "send": "Send",
        "thinking": "Thinking...",
        "sources": "Sources",
    },
}

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

/* Submit button styling */
.stButton > button {
    border-radius: 12px;
    border: 2px solid #000000;
    padding: 8px 14px;
    font-size: 14px;
    font-weight: 600;
    background: #000000;
    color: #ffffff;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    height: 40px;
    min-width: 80px;
}

.stButton > button:hover {
    background: #333333;
    border-color: #333333;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stButton > button:active {
    transform: translateY(1px);
}

/* Spinner styling */
.stSpinner > div {
    border-color: #000000 !important;
    border-width: 3px !important;
    width: 40px !important;
    height: 40px !important;
}

/* Custom spinner container */
.stSpinner {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 20px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
    margin: 20px 0 !important;
}

/* Spinner text styling */
.stSpinner > div + div {
    color: #000000 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    margin-top: 10px !important;
}

/* Language radio in header */
.header-container [data-testid="stRadio"] label {
    font-size: 14px !important;
    color: #000000 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}
.header-container [data-testid="stRadio"] label span,
.header-container [data-testid="stRadio"] label div,
.header-container [data-testid="stRadio"] label p {
    color: #000000 !important;
    opacity: 1 !important;
}
.header-container [data-testid="stRadio"] div[role="radiogroup"] {
    display: flex;
    gap: 8px;
}

/* Language dropdown width in header */
.header-container [data-testid="stSelectbox"] {
    width: 40px !important;
    min-width: 40px !important;
    max-width: 40px !important;
}
.header-container [data-testid="stSelectbox"] > div,
.header-container [data-baseweb="select"],
.header-container [data-baseweb="select"] > div,
.header-container [data-baseweb="select"] div[role="combobox"] {
    width: 40px !important;
    min-width: 40px !important;
    max-width: 40px !important;
    font-size: 12px !important;
    overflow: hidden !important;
    white-space: nowrap !important;
}
.header-container [data-baseweb="select"] div {
    padding: 2px 4px !important;
}
/* Hide caret icon and center value for minimal look */
.header-container [data-baseweb="select"] svg { 
    display: none !important; 
}
.header-container [data-baseweb="select"] div[role="combobox"] { 
    padding-right: 0 !important; 
    justify-content: center !important; 
}
.header-container [data-baseweb="select"] div[role="combobox"] > div { 
    flex: 0 0 auto !important; 
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
        .header-container [data-testid="stRadio"] label {
            font-size: 13px !important;
            color: #000000 !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }
        .header-container [data-testid="stRadio"] label span,
        .header-container [data-testid="stRadio"] label div,
        .header-container [data-testid="stRadio"] label p {
            color: #000000 !important;
            opacity: 1 !important;
        }
    .stButton > button {
        padding: 8px 12px;
        font-size: 14px;
        height: 40px;
        min-width: 80px;
    }
        /* Narrower dropdown on mobile */
        .header-container [data-testid="stSelectbox"],
        .header-container [data-testid="stSelectbox"] > div,
        .header-container [data-baseweb="select"],
        .header-container [data-baseweb="select"] > div,
        .header-container [data-baseweb="select"] div[role="combobox"] {
            width: 40px !important;
            min-width: 40px !important;
            max-width: 40px !important;
            font-size: 12px !important;
            overflow: hidden !important;
            white-space: nowrap !important;
        }
        .header-container [data-baseweb="select"] svg { 
            display: none !important; 
        }
        .header-container [data-baseweb="select"] div[role="combobox"] { 
            padding-right: 0 !important; 
            justify-content: center !important; 
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
    lang = st.session_state.get("lang", "hr")
    label = TRANSLATIONS[lang]["sources"]
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = f"**{label}:**\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


def create_individual_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    lang = st.session_state.get("lang", "hr")
    label = TRANSLATIONS[lang]["sources"]
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = f"\n\n**{label}:**\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i + 1}. {source}\n"
    return sources_string


# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header with language switcher
st.markdown('<div class="header-container">', unsafe_allow_html=True)
# Use container width to avoid truncation on mobile
header_left, header_right = st.columns([0.78, 0.22])
with header_left:
    st.markdown(
        f"""
        <div class="header-title">MeDom Nekretnine</div>
        <div class="header-subtitle">{TRANSLATIONS[st.session_state['lang']]['subtitle']}</div>
        """,
        unsafe_allow_html=True,
    )
with header_right:
    # Dropdown language selector with short labels
    selected_lang = st.selectbox(
        label="Lang",
        options=["HR", "EN"],
        index=0 if st.session_state["lang"] == "hr" else 1,
        label_visibility="collapsed",
        key="lang_switcher_select",
    )
    new_lang = "hr" if selected_lang == "HR" else "en"
    if new_lang != st.session_state["lang"]:
        st.session_state["lang"] = new_lang
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

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

# Create columns for input and button
col1, col2 = st.columns([4, 1])

with col1:
    # Use a unique key that changes when we want to clear the input
    input_key = f"floating_prompt_{st.session_state.get('input_counter', 0)}"
    prompt = st.text_input(
        "",
        placeholder=TRANSLATIONS[st.session_state["lang"]]["search_placeholder"],
        key=input_key,
        label_visibility="collapsed",
    )

with col2:
    submit_button = st.button(
        TRANSLATIONS[st.session_state["lang"]]["send"],
        key=f"submit_{st.session_state.get('input_counter', 0)}",
    )

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Handle prompt submission
if (prompt and not st.session_state.get("clear_input", False)) or submit_button:
    # Get the prompt from the input field
    current_prompt = prompt if prompt else st.session_state.get("current_prompt", "")

    if current_prompt and not st.session_state.get("clear_input", False):
        # Show custom loading indicator for mobile
        st.markdown(f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            border: 2px solid #000000;
        ">
            <div style="
                width: 40px;
                height: 40px;
                border: 4px solid #f3f3f3;
                border-top: 4px solid #000000;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin-right: 15px;
            "></div>
            <div style="
                color: #000000;
                font-weight: 600;
                font-size: 18px;
            ">{TRANSLATIONS[st.session_state['lang']]['thinking']}</div>
        </div>
        <style>
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        </style>
        """, unsafe_allow_html=True)

        generated_response = run_llm(
            query=current_prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )

        formatted_response = (
            f"{generated_response['result']}{create_individual_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(current_prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", current_prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

    # Clear the input by incrementing the counter
    st.session_state["input_counter"] = st.session_state.get("input_counter", 0) + 1
    st.session_state["clear_input"] = True
    st.rerun()

# Reset the clear flag after processing
if st.session_state.get("clear_input", False):
    st.session_state["clear_input"] = False