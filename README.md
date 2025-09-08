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

This project is an interactive web application built with Streamlit that performs advanced Natural Language Processing (NLP) on news articles. It supports multiple languages, can analyze text from various sources, and provides in-depth statistics about the analysis.

### ✨ Core Features

* **Multi-Source Input:** Analyzes articles from pasted text, live URLs, or uploaded `.txt` and `.pdf` files.
* **Robust Error Handling:** Provides clear user feedback when URL fetching fails.
* **AI-Powered Summarization:** Uses a fine-tuned `mT5` model to generate concise summaries of a user-defined length.
* **Multilingual Sentiment Analysis:** Determines sentiment using an efficient `DistilBERT` model.
* **In-Depth Statistics:** Calculates and displays text statistics, including word/character counts, compression rate, and total analysis time.
* **Optimized Performance:** Uses Streamlit's `@st.cache_resource` to load models only once, ensuring a fast and responsive user experience.

### 🛠️ Technology Stack

* **Language:** Python
* **Web Framework:** Streamlit
* **NLP Libraries:** Hugging Face `transformers`, `torch`
* **Text Extraction:** `newspaper3k`, `PyPDF2`
* **Animation:** Custom CSS for dynamic UI elements.

### 🚀 How to Run Locally

1.  **Clone the Repository** and navigate into the project folder.
2.  **Create and activate a virtual environment.**
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```