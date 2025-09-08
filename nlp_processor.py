# nlp_processor.py 

import re
from transformers import pipeline
from langdetect import detect, LangDetectException
from streamlit import cache_resource

# --- NEW: Helper function to clean scraped text ---
def clean_scraped_text(text):
    """Removes common artifacts like author bylines and social media text."""
    # Remove bylines that often start with "By" and are at the start of the text
    text = re.sub(r'^(By|From)[\s\w,]+', '', text.strip())
    # Remove common social media and action words
    junk_words = ['Share', 'Save', 'Email', 'Copy link', 'About sharing']
    for word in junk_words:
        text = text.replace(word, '')
    return text.strip()

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

# --- 2. Cached Model Loading Functions ---
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
        cleaned_text = clean_scraped_text(text) # <-- APPLY CLEANING
        summarizer = get_summarizer()
        summary_result = summarizer(cleaned_text, min_length=80, max_length=250)
        summary_text = summary_result[0]['summary_text']
        cleaned_summary = re.sub(r'<extra_id_\d+>', '', summary_text).strip()
        return cleaned_summary, None
    except Exception as e:
        return None, f"Summarization failed: {e}"

def analyze_sentiment(text):
    """Analyzes sentiment using the cached model."""
    try:
        cleaned_text = clean_scraped_text(text) # <-- APPLY CLEANING
        sentiment_analyzer = get_sentiment_analyzer()
        truncated_text = cleaned_text[:1000]
        result = sentiment_analyzer(truncated_text)
        sentiment_label = result[0]['label'].capitalize()
        sentiment_score = result[0]['score']
        return sentiment_label, sentiment_score, None
    except Exception as e:
        return None, None, f"Sentiment analysis failed: {e}"