# Personalized News Summarizer: An AI-Powered System for Automated Article Extraction, Summarization, and Evaluation

## 1. Project Overview

This project implements a web-based **Personalized News Summarizer**.  
Users paste a news article URL or raw text, and the system:

1. Fetches and cleans the article content.
2. Generates an abstractive summary using a pre-trained transformer model.
3. Automatically evaluates the summary quality with ROUGE and BERTScore.
4. Displays all results in a clean, browser-based UI.

The goal is to help users quickly digest long news articles while keeping key information and providing transparent summary quality metrics.

## 2. Tech Stack

- **Backend:** Python, Flask  
- **NLP Models:** Hugging Face `transformers` (T5 / PEGASUS-style models)  
- **Scraping:** `requests`, `BeautifulSoup`  
- **Evaluation:** `rouge-score`, `bert-score`  
- **Frontend:** HTML, CSS, vanilla JavaScript  
- **Environment:** Python virtual environment (`venv`), tested on macOS

## 3. Project Structure

```text
personalized-news-summarizer/
│
├── app/
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── api.py            # Flask API endpoints (health, summarize)
│   │   ├── scraper.py        # Article fetching and HTML parsing
│   │   ├── summarizer.py     # Transformer-based summarization pipeline
│   │   └── evaluation.py     # ROUGE and BERTScore evaluation
│   │
│   └── frontend/
│       ├── index.html        # Single-page UI
│       ├── script.js         # Frontend logic & API calls
│       └── style.css         # Basic styling
│
├── run.py                    # Flask app entry point
├── requirements.txt          # Python dependencies
├── test_summary.py           # Local debugging script for summarization
└── .gitignore                # Ignore venv, IDE files, etc.
```

## 4. Setup & Installation

1. Clone the repository
git clone https://github.com/Arph003/personalized-news-summarizer.git

cd personalized-news-summarizer

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On macOS / Linux
.\venv\Scripts\activate  # On Windows (if needed)

3. Install dependencies
pip install -r requirements.txt

## 5. Running the Application
   
5.1 Start the Flask backend
cd /path/to/personalized-news-summarizer
source venv/bin/activate
python run.py

You should see something like:
 * Running on http://127.0.0.1:5000

5.2 Open the web UI

Open app/frontend/index.html in a browser, or

Use a simple static file server if needed.

In the UI:

Paste a news article URL into the "Article URL" field, or

Paste raw article text into the "Raw Text" field.

Click Summarize.

The right panel will display:

Source metadata (title, domain, URL)

Generated summary

Meta information (lengths, compression ratio)

Evaluation metrics (ROUGE-1/2/Lsum, BERTScore)

Truncated original text

<img width="1101" height="788" alt="website_demo" src="https://github.com/user-attachments/assets/8a05be08-bb1c-44dd-993f-c2d4da6daf7a" />

## 6. API Endpoints

The backend exposes a small JSON API:
GET /api/health

Health check.

Response:
{ "status": "ok" }

POST /api/summarize

Generate a summary and evaluation for a given article.

Request body:
{
  "url": "https://www.ibm.com/think/topics/foundation-models"
  // or: "text": "raw article text ..."
}

Response (simplified):
{
  "success": true,
  "source": {
    "title": "...",
    "domain": "...",
    "url": "..."
  },
  "content": {
    "original_text": "...",
    "summary": "..."
  },
  "evaluation": {
    "rouge1": { "f1": 0.0437, "precision": 1.0, "recall": 0.0223 },
    "rouge2": { ... },
    "rougeLsum": { ... },
    "bertscore": { "f1": 0.40, "precision": 0.76, "recall": 0.20 },
    "runtime_ms": 4400,
    "word_counts": { "original": 1643, "summary": 41 }
  },
  "meta": {
    "compression_ratio": 0.023,
    "original_length": 11364,
    "summary_length": 265
  }
}

## 7. Evaluation Details

The system currently supports:

ROUGE-1, ROUGE-2, ROUGE-Lsum (F1 / P / R)

BERTScore (F1 / P / R) with a standard multilingual encoder

Evaluation is performed against the original article text to estimate:

Content overlap (ROUGE)

Semantic similarity (BERTScore)

Length/compression statistics

These metrics are surfaced in the UI to increase transparency of the summarization quality.

## 8. Demo Video & Report & Website

Demo Video (≤ 5 minutes): https://youtu.be/PIs8AA1-tmQ

Project Report (PDF): https://github.com/Arph003/personalized-news-summarizer/blob/main/Final_Report.pdf 

Website: https://arph003.github.io/personalized-news-summarizer/

Both links will be added here and in the course submission portal.

## 9. Team

Zhiqi Li

Yuan Tian

(Team name: GoodTeam)
