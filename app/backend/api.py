# app/backend/api.py

import time
from flask import Blueprint, request, jsonify
from app.backend.scraper import fetch_article
from app.backend.summarizer import summarize_text
from app.backend.evaluation import evaluate_summary


api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200


@api_bp.route("/summarize", methods=["POST"])
def summarize_endpoint():
    """
    Request body (JSON):
    {
        "url": "https://example.com/news-article",
        "text": "optional raw text if you want to bypass scraping"
    }

    At least one of "url" or "text" must be provided.
    """
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    raw_text = data.get("text")

    if not url and not raw_text:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Either 'url' or 'text' must be provided in the request body.",
                }
            ),
            400,
        )

    article = None

    # If URL is provided, try to fetch and extract article text
    if url:
        article = fetch_article(url)
        if not article.get("success"):
            # If scraping failed and there is no fallback text, return error
            if not raw_text:
                return (
                    jsonify(
                        {
                            "success": False,
                            "source": {
                                "url": url,
                                "domain": article.get("domain"),
                                "title": article.get("title"),
                            },
                            "error": article.get("error")
                            or "Failed to fetch article content from the given URL.",
                        }
                    ),
                    502,
                )
        else:
            raw_text = article.get("text", "")

    if not raw_text or not raw_text.strip():
        return (
            jsonify(
                {
                    "success": False,
                    "source": {
                        "url": url,
                        "domain": article.get("domain") if article else None,
                        "title": article.get("title") if article else None,
                    },
                    "error": "No usable text content was found for summarization.",
                }
            ),
            400,
        )

    # Measure summarization runtime
    start_time = time.time()
    summary = summarize_text(raw_text)
    end_time = time.time()
    runtime_ms = int((end_time - start_time) * 1000)

    original_length = len(raw_text)
    summary_length = len(summary) if summary is not None else 0
    compression_ratio = (
        round(summary_length / original_length, 3)
        if original_length > 0
        else None
    )

    # Evaluation metrics (ROUGE etc.)
    eval_scores = evaluate_summary(raw_text, summary)

    response = {
        "success": True,
        "source": {
            "url": url,
            "domain": article.get("domain") if article else None,
            "title": article.get("title") if article else None,
        },
        "content": {
            "original_text": raw_text,
            "summary": summary,
        },
        "meta": {
            "original_length": original_length,
            "summary_length": summary_length,
            "compression_ratio": compression_ratio,
        },
        "evaluation": {
            **eval_scores,
            "runtime_ms": runtime_ms,
        },
    }

    return jsonify(response), 200
