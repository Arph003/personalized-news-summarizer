# app/backend/evaluation.py

from typing import Any, Dict
from rouge_score import rouge_scorer
from bert_score import score as bertscore_score


def _convert_rouge(rouge_res) -> Dict[str, float]:
    return {
        "precision": round(rouge_res.precision, 4),
        "recall": round(rouge_res.recall, 4),
        "f1": round(rouge_res.fmeasure, 4),
    }


def _compute_bertscore(original: str, candidate: str) -> Dict[str, float] | None:
    """
    Compute BERTScore between original article text and generated summary.

    NOTE:
    In a perfect setup we would compare the system summary against a human
    reference summary. Here we treat the original article as a pseudo
    reference, which is only an approximation but still gives a useful
    similarity signal.
    """
    try:
        # Use a relatively lightweight English model for speed.
        P, R, F1 = bertscore_score(
            [candidate],
            [original],
            lang="en",
            model_type="bert-base-uncased",
            rescale_with_baseline=True,
        )

        return {
            "precision": round(float(P.mean().item()), 4),
            "recall": round(float(R.mean().item()), 4),
            "f1": round(float(F1.mean().item()), 4),
        }
    except Exception:
        # If anything goes wrong (e.g. model download error),
        # we simply return None so that the API can still respond.
        return None


def evaluate_summary(original_text: str, summary: str) -> Dict[str, Any]:
    """
    Compute automatic evaluation metrics for a generated summary.
    This includes ROUGE scores, simple word statistics, vocabulary
    coverage, and BERTScore.
    """
    original = (original_text or "").strip()
    candidate = (summary or "").strip()

    if not original or not candidate:
        return {
            "rouge1": None,
            "rouge2": None,
            "rougeLsum": None,
            "word_counts": {
                "original": len(original.split()) if original else 0,
                "summary": len(candidate.split()) if candidate else 0,
            },
            "vocab_coverage": None,
            "bertscore": None,
        }

    # Basic word statistics
    original_words = original.split()
    summary_words = candidate.split()

    word_counts = {
        "original": len(original_words),
        "summary": len(summary_words),
    }

    # Vocabulary overlap: how much of the summary vocabulary also appears in the article
    original_vocab = set(original_words)
    summary_vocab = set(summary_words)
    overlap = len(original_vocab & summary_vocab)
    vocab_coverage = round(overlap / max(1, len(summary_vocab)), 4)

    # ROUGE scores
    scorer = rouge_scorer.RougeScorer(
        ["rouge1", "rouge2", "rougeLsum"],
        use_stemmer=True,
    )
    scores = scorer.score(original, candidate)

    rouge1 = _convert_rouge(scores["rouge1"])
    rouge2 = _convert_rouge(scores["rouge2"])
    rouge_lsum = _convert_rouge(scores["rougeLsum"])

    # BERTScore
    bertscore = _compute_bertscore(original, candidate)

    return {
        "rouge1": rouge1,
        "rouge2": rouge2,
        "rougeLsum": rouge_lsum,
        "word_counts": word_counts,
        "vocab_coverage": vocab_coverage,
        "bertscore": bertscore,
    }
