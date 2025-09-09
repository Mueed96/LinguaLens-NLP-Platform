# 🌐 LinguaLens: A Multilingual News Analysis Platform

**Author:** Abdul Mueed

*🔎 Bringing Clarity to Global News.*

---

This project is a sophisticated, interactive web application built with Streamlit that performs advanced Natural Language Processing (NLP) on news articles. It supports multiple languages, can analyze text from various sources, and provides in-depth statistics about the analysis.

### ✨ Core Features

* **Multi-Source Input:** Analyzes articles from four different sources: pasted text, live URLs, uploaded files (`.txt`, `.pdf`), and **RSS feeds**.
* **Automatic Language Detection:** Identifies the language of the article using the `langdetect` library.
* **High-Quality Summarization:** Uses the powerful `csebuetnlp/mT5_multilingual_XLSum` model to generate concise, abstractive summaries in multiple languages.
* **Multilingual Sentiment Analysis:** Determines the sentiment (Positive, Negative, Neutral) using an efficient `DistilBERT` model.
* **In-Depth Statistics:** Calculates and displays text statistics, including word/character counts, compression rate, and total analysis time.
* **Optimized Performance:** Uses Streamlit's `@st.cache_resource` to load models only once, ensuring a fast and responsive user experience.
* **Dynamic UI:** Features a custom, animated header and a clean, tabbed interface for a modern user experience.

### 🛠️ Technology Stack

* **Language:** Python
* **Web Framework:** Streamlit
* **NLP Libraries:** Hugging Face `transformers`, `torch`
* **Text Extraction:** `newspaper3k`, `PyPDF2`, `feedparser`
* **Deployment:** GitHub (Code), Hugging Face Spaces (Live App)

### 🚧 Challenges & Solutions

This project involved overcoming several real-world engineering challenges:

* **Memory Management:** The initial choice of high-quality models exceeded the memory limits of free cloud hosting platforms. This was solved by strategically selecting more memory-efficient models and ultimately choosing Hugging Face Spaces for its more generous free-tier resources.
* **Web Scraping Reliability:** The `newspaper3k` library proved unreliable for some modern news websites. Robust error handling was implemented in the UI to gracefully manage fetch failures and inform the user.
* **Deployment & Versioning:** Debugged several deployment issues, including Python version conflicts in the `requirements.txt` file and Git authentication/LFS problems. The solution was to create a flexible requirements file and use a proper Git workflow for pushing to multiple remotes.

### 🚀 How to Run Locally

1.  Clone the repository and navigate into the project folder.
2.  Create and activate a virtual environment.
3.  Install dependencies: `pip install -r requirements.txt`
4.  Run the Streamlit App: `streamlit run app.py`