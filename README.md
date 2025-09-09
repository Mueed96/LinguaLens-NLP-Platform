---
title: LinguaLens
emoji: 🌐
colorFrom: blue
colorTo: green
sdk: streamlit
app_file: app.py
---

# 🌐 LinguaLens: A Multilingual News Analysis Platform

**Author:** Abdul Mueed

*🔎 Bringing Clarity to Global News.*

---

This project is a sophisticated, interactive web application built with Streamlit that performs advanced Natural Language Processing (NLP) on news articles. It supports multiple languages, can analyze text from various sources, and provides in-depth statistics about the analysis.

### ✨ Core Features

* **Multi-Source Input:** Analyzes articles from four different sources: pasted text, live URLs, uploaded files (`.txt`, `.pdf`), and RSS feeds.
* **Automatic Language Detection:** Identifies the language of the article.
* **High-Quality Summarization:** Uses the powerful `csebuetnlp/mT5_multilingual_XLSum` model to generate concise summaries.
* **Multilingual Sentiment Analysis:** Determines sentiment using an efficient `DistilBERT` model.
* **In-Depth Statistics:** Calculates and displays text statistics, including word/character counts, compression rate, and total analysis time.
* **Optimized Performance:** Uses Streamlit's `@st.cache_resource` to load models only once, ensuring a fast and responsive user experience.

### 🛠️ Technology Stack

* **Language:** Python
* **Web Framework:** Streamlit
* **NLP Libraries:** Hugging Face `transformers`, `torch`
* **Text Extraction:** `newspaper3k`, `PyPDF2`, `feedparser`
* **Deployment:** GitHub (Code), Hugging Face Spaces (Live App)

### 🚀 How to Run Locally

1.  Clone the repository and navigate into the project folder.
2.  Create and activate a virtual environment.
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run the Streamlit App: `streamlit run app.py`