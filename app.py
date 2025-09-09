# app.py

import streamlit as st
import time
from ingestion import get_text_from_url, get_text_from_pdf, get_text_from_txt, parse_rss_feed
from nlp_processor import detect_language, summarize_text, analyze_sentiment

# --- Helper Functions ---
def calculate_statistics(original_text, summary_text):
    original_words = len(original_text.split())
    original_chars = len(original_text)
    summary_words = len(summary_text.split())
    if original_words > 0:
        compression_rate = (1 - (summary_words / original_words)) * 100
    else:
        compression_rate = 0
    return {
        "original_words": original_words,
        "original_chars": original_chars,
        "summary_words": summary_words,
        "compression_rate": compression_rate
    }

def format_time(seconds):
    """Converts seconds into a more readable minutes and seconds string."""
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    if minutes > 0:
        return f"{minutes} min {remaining_seconds} sec"
    else:
        return f"{remaining_seconds} sec"

# --- Page Configuration ---
st.set_page_config(
    page_title="LinguaLens",
    page_icon="✨",
    layout="wide"
)

# --- State Initialization ---
if 'article_text' not in st.session_state:
    st.session_state.article_text = ""
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'rss_articles' not in st.session_state:
    st.session_state.rss_articles = []

# --- Centered Header ---
with st.container():
    st.markdown("<h1 style='text-align: center;'><span class='spinning-globe'>🌐</span> LinguaLens</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>🔎 <i>Bringing Clarity to Global News.</i></h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>A Project By Abdul Mueed</p>", unsafe_allow_html=True)

# --- CSS for Spinning Animation ---
st.markdown("""
<style>
@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
.spinning-globe {
    display: inline-block;
    animation: spin 8s linear infinite;
}
</style>
""", unsafe_allow_html=True)

st.divider()

# --- Input Section ---
with st.container():
    st.header("📥 Provide an Article to Analyze")
    
    tab1, tab2, tab3, tab4 = st.tabs(["✍️ Paste Text", "🔗 URL", "📄 File Upload", "📰 RSS Feed"])

    with tab1:
        pasted_text = st.text_area("Paste the article text below:", height=250, key="pasted_text")
        if st.button("Load Text", use_container_width=True, type="primary"):
            st.session_state.article_text = pasted_text
            st.session_state.analysis_results = None
            st.toast("Text loaded!", icon="✅")

    with tab2:
        url_input = st