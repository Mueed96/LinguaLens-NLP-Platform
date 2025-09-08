# nlp_processor.py

import re
from transformers import pipeline
from langdetect import detect, LangDetectException
from streamlit import cache_resource

# --- 1. Language Detection Function ---
def detect_language(text):
    """Analyzes the text and returns the detected language code."""
    try:
        if len(text.strip()) < 20:
            return "unknown", "Text too short for reliable language detection."
        lang_code = detect(text)
        return lang_code, None
    except LangDetectException:
        return "unknown", "Language could not be reliably detected."

# --- 2. Cached Model Loading Functions (for performance) ---
@cache_resource
def get_summarizer():
    """Loads the high-quality multilingual summarization model into cache."""
    print("Loading summarization model...")
    return pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")

@cache_resource
def get_sentiment_analyzer():
    """Loads the memory-efficient sentiment model into cache."""
    print("Loading sentiment analysis model...")
    return pipeline("sentiment-analysis", model="lxyuan/distilbert-base-multilingual-cased-sentiments-student")

# --- 3. NLP Processing Functions ---
def summarize_text(text, lang_code):
    """Generates a summary using the cached model."""
    try:
        summarizer = get_summarizer()
        summary_result = summarizer(text, min_length=80, max_length=250)
        
        # Clean the summary text to remove any model artifacts
        summary_text = summary_result[0]['summary_text']
        cleaned_summary = re.sub(r'<extra_id_\d+>', '', summary_text).strip()
        
        return cleaned_summary, None
    except Exception as e:
        return None, f"Summarization failed: {e}"

def analyze_sentiment(text):
    """Analyzes sentiment using the cached model."""
    try:
        sentiment_analyzer = get_sentiment_analyzer()
        truncated_text = text[:1000]
        result = sentiment_analyzer(truncated_text)
        sentiment_label = result[0]['label'].capitalize()
        sentiment_score = result[0]['score']
        return sentiment_label, sentiment_score, None
    except Exception as e:
        return None, None, f"Sentiment analysis failed: {e}"