# Personalized News Summarizer: An AI-Powered System for Automated Article Extraction, Summarization, and Evaluation

## 1. Project Overview

The **Personalized News Summarizer** is a web-based application that helps users quickly understand long news articles.
Given a URL to an online article, the system:

1. Fetches and cleans the article text (web scraping).
2. Generates an abstractive summary using a pre-trained transformer model (T5-small).
3. Evaluates the summary with automatic metrics (ROUGE and BERTScore).
4. Displays the original article, summary, and evaluation results in a clean web interface.

The goal is to make real-world news consumption faster, more transparent, and more user-centric by combining modern NLP models with a lightweight, explainable evaluation pipeline.

---

## 2. Features

- 📰 **URL-based article ingestion** – Paste any supported news URL and fetch the main article content.
- ✂️ **Abstractive summarization** – Generate concise summaries using a T5-small transformer model.
- 📊 **Automatic evaluation** – Compute ROUGE-1 / ROUGE-2 / ROUGE-L and BERTScore to assess summary quality.
- 📉 **Extra analytics** – Show compression ratio, word counts, vocabulary coverage, and runtime.
- 🌐 **Web-based UI** – Minimal, responsive interface for entering URLs and viewing results.
- 🧩 **Modular design** – Clear separation between scraping, summarization, evaluation, and frontend.

---

## 3. Tech Stack

- **Backend**
  - Python 3.12
  - Flask (REST API)
  - Requests, BeautifulSoup4 (web scraping)
  - Hugging Face Transformers (T5-small)
  - PyTorch (model execution, MPS-enabled on macOS)
  - rouge-score, bert-score (evaluation)

- **Frontend**
  - HTML / CSS / JavaScript
  - Fetch-based calls to the Flask API

---

## 4. Project Structure

```text
personalized-news-summarizer/
├── app/
│   ├── __init__.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── scraper.py        # Fetch and clean article text from a URL
│   │   ├── summarizer.py     # T5-small summarization pipeline
│   │   └── evaluation.py     # ROUGE + BERTScore + extra metrics
│   └── frontend/
│       ├── index.html        # Main UI page
│       ├── script.js         # Frontend logic and API calls
│       └── styles.css        # (If present) Styling for the UI
├── requirements.txt          # Python dependencies
├── run.py                    # Flask app entry point
└── README.md                 # Project documentation (this file)
