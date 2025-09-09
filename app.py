# app.py (DEFINITIVE FINAL VERSION with All Fixes)

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
        url_input = st.text_input("Enter the news article URL:", key="url_input")
        if st.button("Fetch from URL", use_container_width=True, type="primary"):
            if url_input:
                with st.spinner("Fetching article..."):
                    fetched_text = get_text_from_url(url_input)
                    st.session_state.analysis_results = None
                    if fetched_text:
                        st.session_state.article_text = fetched_text
                        st.toast("Article fetched successfully!", icon="✅")
                    else:
                        st.session_state.article_text = ""
                        st.error("Failed to fetch article. Please try a different URL or paste the text directly.")
            else:
                st.warning("Please enter a URL.")

    with tab3:
        uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["txt", "pdf"])
        if uploaded_file:
            with st.spinner("Processing file..."):
                if uploaded_file.type == "text/plain":
                    st.session_state.article_text = get_text_from_txt(uploaded_file)
                else:
                    st.session_state.article_text = get_text_from_pdf(uploaded_file)
                st.session_state.analysis_results = None
                st.toast("File loaded!", icon="📄")

    with tab4:
        feed_url = st.text_input("Enter RSS feed URL", placeholder="e.g., http://feeds.bbci.co.uk/news/world/rss.xml")
        if st.button("Fetch Feed", use_container_width=True):
            with st.spinner("Fetching articles from feed..."):
                st.session_state.rss_articles = parse_rss_feed(feed_url)
                if not st.session_state.rss_articles:
                    st.error("Could not fetch articles. Please check the RSS feed URL.")
        
        if st.session_state.rss_articles:
            article_titles = [article['title'] for article in st.session_state.rss_articles]
            selected_index = st.selectbox("Select an article from the feed:", options=range(len(article_titles)), format_func=lambda i: article_titles[i])
            
            if st.button("Load Selected Article", use_container_width=True, type="primary"):
                selected_link = st.session_state.rss_articles[selected_index]['link']
                if selected_link:
                    with st.spinner("Fetching full article text..."):
                        # --- THIS SECTION IS THE FINAL FIX ---
                        fetched_text = get_text_from_url(selected_link)
                        st.session_state.analysis_results = None

                        if fetched_text:
                            st.session_state.article_text = fetched_text
                            st.toast("Article loaded!", icon="✅")
                        else:
                            st.session_state.article_text = ""
                            st.error("Failed to fetch this specific article. The website may be blocking the scraper. Please try a different article from the feed.")

st.divider()

# --- Analysis Trigger and Results Display ---
if st.session_state.article_text:
    st.header("🚀 Review and Analyze")
    
    with st.expander("Click to view the loaded article text"):
        st.text_area("", st.session_state.article_text, height=300)

    if st.button("✨ Analyze Now!", use_container_width=True, type="primary"):
        with st.spinner("Our AI is working its magic... ✨"):
            start_time = time.time()
            text = st.session_state.article_text
            lang_code, lang_error = detect_language(text)
            summary, summary_error = summarize_text(text, lang_code)
            sentiment_label, sentiment_score, sentiment_error = analyze_sentiment(text)
            stats = calculate_statistics(text, summary)
            end_time = time.time()
            analysis_duration = end_time - start_time
            
            st.session_state.analysis_results = {
                "lang_code": lang_code, "lang_error": lang_error,
                "summary": summary, "summary_error": summary_error,
                "sentiment_label": sentiment_label, "sentiment_score": sentiment_score, "sentiment_error": sentiment_error,
                "stats": stats,
                "analysis_time": analysis_duration
            }

if st.session_state.analysis_results:
    st.divider()
    st.header("📊 Read the Analysis")
    results = st.session_state.analysis_results
    
    res_tab1, res_tab2, res_tab3, res_tab4, res_tab5 = st.tabs([
        "📖 Summary", "😊 Sentiment", "🌐 Language", "📊 Statistics", "📄 Original Text"
    ])
    
    # ... (rest of the results display is unchanged)
    with res_tab1:
        st.subheader("Generated Article Summary")
        if not results["summary_error"]:
            st.success(results["summary"])
        else:
            st.error("Summarization failed.")

    with res_tab2:
        st.subheader("Sentiment Analysis")
        if not results["sentiment_error"]:
            with st.container(border=True):
                st.metric(label="Detected Sentiment", value=results["sentiment_label"])
                st.progress(results["sentiment_score"], text=f"Confidence Score: {results['sentiment_score']:.1%}")
        else:
            st.error("Sentiment analysis failed.")

    with res_tab3:
        st.subheader("Language Detection")
        if not results["lang_error"]:
            with st.container(border=True):
                st.metric(label="Detected Language", value=results["lang_code"].upper())
        else:
            st.error("Language detection failed.")
            
    with res_tab4:
        st.subheader("Analysis Statistics")
        stats = results["stats"]
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)

        with row1_col1:
            with st.container(border=True):
                st.metric("Original Words", f'{stats["original_words"]:,}')
        with row1_col2:
            with st.container(border=True):
                st.metric("Original Chars", f'{stats["original_chars"]:,}')
        with row2_col1:
            with st.container(border=True):
                st.metric("Summary Words", f'{stats["summary_words"]:,}')
        with row2_col2:
            with st.container(border=True):
                st.metric("Compression Rate", f'{stats["compression_rate"]:.1f}%')
        st.divider()
        with st.container(border=True):
             formatted_time = format_time(results['analysis_time'])
             st.metric("⏱️ Analysis Time", formatted_time)
            
    with res_tab5:
        st.subheader("Original Full Text")
        st.text_area("", st.session_state.article_text, height=400)

elif not st.session_state.article_text:
    st.info("Your analyzed article results will appear here once you provide a source.")