// app/frontend/script.js

const urlInput = document.getElementById("url-input");
const textInput = document.getElementById("text-input");
const summarizeBtn = document.getElementById("summarize-btn");
const statusMessage = document.getElementById("status-message");

const sourceInfo = document.getElementById("source-info");
const sourceTitle = document.getElementById("source-title");
const sourceDomain = document.getElementById("source-domain");
const sourceUrl = document.getElementById("source-url");

const summaryCard = document.getElementById("summary-card");
const summaryText = document.getElementById("summary-text");

const metaCard = document.getElementById("meta-card");
const metaOriginalLength = document.getElementById("meta-original-length");
const metaSummaryLength = document.getElementById("meta-summary-length");
const metaCompressionRatio = document.getElementById("meta-compression-ratio");

const evaluationCard = document.getElementById("evaluation-card");
const evalRouge1F1 = document.getElementById("eval-rouge1-f1");
const evalRouge1PR = document.getElementById("eval-rouge1-pr");
const evalRouge2F1 = document.getElementById("eval-rouge2-f1");
const evalRouge2PR = document.getElementById("eval-rouge2-pr");
const evalRougeLF1 = document.getElementById("eval-rougeL-f1");
const evalRougeLPR = document.getElementById("eval-rougeL-pr");
const evalBertF1 = document.getElementById("eval-bertscore-f1");
const evalBertPR = document.getElementById("eval-bertscore-pr");
const evalWordCounts = document.getElementById("eval-word-counts");
const evalVocabCoverage = document.getElementById("eval-vocab-coverage");
const evalRuntime = document.getElementById("eval-runtime");

const originalCard = document.getElementById("original-card");
const originalText = document.getElementById("original-text");
const toggleOriginalBtn = document.getElementById("toggle-original-btn");


function clearOutput() {
    sourceInfo.classList.add("hidden");
    summaryCard.classList.add("hidden");
    metaCard.classList.add("hidden");
    evaluationCard.classList.add("hidden");
    originalCard.classList.add("hidden");

    sourceTitle.textContent = "";
    sourceDomain.textContent = "";
    sourceUrl.textContent = "";

    summaryText.textContent = "";
    metaOriginalLength.textContent = "";
    metaSummaryLength.textContent = "";
    metaCompressionRatio.textContent = "";

    evalRouge1F1.textContent = "";
    evalRouge1PR.textContent = "";
    evalRouge2F1.textContent = "";
    evalRouge2PR.textContent = "";
    evalRougeLF1.textContent = "";
    evalRougeLPR.textContent = "";
    evalWordCounts.textContent = "";
    evalVocabCoverage.textContent = "";
    evalRuntime.textContent = "";
    evalBertF1.textContent = "";
    evalBertPR.textContent = "";

    originalText.textContent = "";

    statusMessage.textContent = "";
    statusMessage.className = "status-message";
}


function setStatus(message, type = "info") {
    statusMessage.textContent = message;
    statusMessage.className = "status-message " + type;
}


function formatNumber(value, digits = 4) {
    if (value == null || isNaN(value)) {
        return "-";
    }
    return Number(value).toFixed(digits);
}


function formatPercent(value, digits = 1) {
    if (value == null || isNaN(value)) {
        return "-";
    }
    return (Number(value) * 100).toFixed(digits) + "%";
}


async function callSummarizer() {
    clearOutput();

    const url = urlInput.value.trim();
    const rawText = textInput.value.trim();

    if (!url && !rawText) {
        setStatus("Please provide at least a URL or some raw text.", "error");
        return;
    }

    // Disable button during request
    summarizeBtn.disabled = true;
    summarizeBtn.textContent = "Summarizing...";
    setStatus("Calling backend summarization API...", "info");

    try {
        const payload = {};
        if (url) {
            payload.url = url;
        }
        if (rawText) {
            payload.text = rawText;
        }

        const resp = await fetch("/api/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!resp.ok) {
            const errorText = await resp.text();
            console.error("HTTP error:", resp.status, errorText);
            setStatus(`Request failed with status ${resp.status}`, "error");
            return;
        }

        const data = await resp.json();
        console.log("Summarizer response:", data);

        if (!data.success) {
            setStatus(data.error || "Summarization failed.", "error");
            return;
        }

        // Show source info
        const src = data.source || {};
        if (src.title || src.domain || src.url) {
            sourceTitle.textContent = src.title || "-";
            sourceDomain.textContent = src.domain || "-";
            if (src.url) {
                sourceUrl.textContent = src.url;
                sourceUrl.href = src.url;
            } else {
                sourceUrl.textContent = "-";
                sourceUrl.removeAttribute("href");
            }
            sourceInfo.classList.remove("hidden");
        }

        // Show summary
        const content = data.content || {};
        summaryText.textContent = content.summary || "(Empty summary)";
        summaryCard.classList.remove("hidden");

        // Show meta
        const meta = data.meta || {};
        metaOriginalLength.textContent = meta.original_length ?? "-";
        metaSummaryLength.textContent = meta.summary_length ?? "-";
        if (meta.compression_ratio != null) {
            const percentage = (meta.compression_ratio * 100).toFixed(1);
            metaCompressionRatio.textContent = `${meta.compression_ratio} (${percentage}%)`;
        } else {
            metaCompressionRatio.textContent = "-";
        }
        metaCard.classList.remove("hidden");

        // Show evaluation
        const evalData = data.evaluation || {};
        const rouge1 = evalData.rouge1 || {};
        const rouge2 = evalData.rouge2 || {};
        const rougeL = evalData.rougeLsum || {};
        const wordCounts = evalData.word_counts || {};
        const bert = evalData.bertscore || {};


        evalRouge1F1.textContent = formatNumber(rouge1.f1);
        if (rouge1.precision != null && rouge1.recall != null) {
            evalRouge1PR.textContent = `P/R: ${formatNumber(rouge1.precision)} / ${formatNumber(rouge1.recall)}`;
        }

        evalRouge2F1.textContent = formatNumber(rouge2.f1);
        if (rouge2.precision != null && rouge2.recall != null) {
            evalRouge2PR.textContent = `P/R: ${formatNumber(rouge2.precision)} / ${formatNumber(rouge2.recall)}`;
        }

        evalRougeLF1.textContent = formatNumber(rougeL.f1);
        if (rougeL.precision != null && rougeL.recall != null) {
            evalRougeLPR.textContent = `P/R: ${formatNumber(rougeL.precision)} / ${formatNumber(rougeL.recall)}`;
        }

        // BERTScore
        evalBertF1.textContent = formatNumber(bert.f1);
        if (bert.precision != null && bert.recall != null) {
            evalBertPR.textContent =
                `P/R: ${formatNumber(bert.precision)} / ${formatNumber(bert.recall)}`;
        } else {
            evalBertPR.textContent = "";
        }

        if (wordCounts.original != null || wordCounts.summary != null) {
            const orig = wordCounts.original ?? "-";
            const summ = wordCounts.summary ?? "-";
            evalWordCounts.textContent = `${orig} / ${summ}`;
        } else {
            evalWordCounts.textContent = "-";
        }

        if (evalData.vocab_coverage != null) {
            evalVocabCoverage.textContent =
                `${formatNumber(evalData.vocab_coverage)} (${formatPercent(evalData.vocab_coverage)})`;
        } else {
            evalVocabCoverage.textContent = "-";
        }

        if (evalData.runtime_ms != null) {
            evalRuntime.textContent = `${evalData.runtime_ms} ms`;
        } else {
            evalRuntime.textContent = "-";
        }

        evaluationCard.classList.remove("hidden");

        // Show truncated original text
        if (content.original_text) {
            const maxPreview = 2000;
            let displayText = content.original_text;
            if (displayText.length > maxPreview) {
                displayText = displayText.slice(0, maxPreview) + "\n\n[Truncated for display...]";
            }
            originalText.textContent = displayText;
            originalCard.classList.remove("hidden");
        }

        setStatus("Summarization completed successfully.", "success");
    } catch (err) {
        console.error("Error calling summarizer:", err);
        setStatus("An unexpected error occurred while calling the API.", "error");
    } finally {
        summarizeBtn.disabled = false;
        summarizeBtn.textContent = "Summarize";
    }
}


summarizeBtn.addEventListener("click", () => {
    callSummarizer();
});

toggleOriginalBtn.addEventListener("click", () => {
    if (originalText.style.display === "none" || !originalText.style.display) {
        originalText.style.display = "block";
        toggleOriginalBtn.textContent = "Hide";
    } else {
        originalText.style.display = "none";
        toggleOriginalBtn.textContent = "Show";
    }
});

// Hide original text by default
originalText.style.display = "none";
