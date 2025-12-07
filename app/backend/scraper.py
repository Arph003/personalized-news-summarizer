# app/backend/scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def fetch_article_html(url: str, timeout: int = 10) -> str:
    """
    Fetch raw HTML of a page.
    Raises requests.exceptions.RequestException on network errors.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def extract_main_text(html: str) -> dict:
    """
    Try to extract title and main article text from HTML using simple heuristics.
    Returns a dict: {"title": str, "text": str}
    """
    soup = BeautifulSoup(html, "html.parser")

    # ---- 1. 标题 ----
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            title = h1.get_text(strip=True)

    # ---- 2. 正文候选段落 ----
    paragraphs = []

    article = soup.find("article")
    if article:
        paragraphs = article.find_all("p")

    # 如果 <article> 里找不到，再按 class 关键词找
    if not paragraphs:
        candidates = soup.find_all(
            ["div", "section"],
            class_=lambda c: c
            and any(
                kw in c.lower()
                for kw in ["article", "content", "story", "post", "main"]
            ),
        )
        if candidates:
            best = max(candidates, key=lambda c: len(c.find_all("p")))
            paragraphs = best.find_all("p")

    # 再不行就用全页所有 <p>
    if not paragraphs:
        paragraphs = soup.find_all("p")

    texts = []
    for p in paragraphs:
        txt = p.get_text(" ", strip=True)
        # 把阈值放宽一点，只要不是特别短就收
        if len(txt) > 20:
            texts.append(txt)

    # 如果还是太少，就直接把前 10 段拼起来，尽量给点内容
    if len(texts) < 3:
        fallback_texts = []
        for p in paragraphs[:10]:
            t = p.get_text(" ", strip=True)
            if t:
                fallback_texts.append(t)
        if fallback_texts:
            texts = fallback_texts

    body = "\n\n".join(texts).strip()

    return {
        "title": title or "",
        "text": body or "",
    }


def fetch_article(url: str) -> dict:
    """
    High-level helper:
    输入 URL → 返回 { "url", "domain", "title", "text", "success", "error"(可选) }
    """
    try:
        html = fetch_article_html(url)
        extracted = extract_main_text(html)
        parsed = urlparse(url)

        text = extracted.get("text", "").strip()
        title = extracted.get("title", "").strip()

        if not text:
            return {
                "success": False,
                "url": url,
                "domain": parsed.netloc,
                "title": title,
                "text": "",
                "error": "Could not extract any meaningful article text from the page.",
            }

        return {
            "success": True,
            "url": url,
            "domain": parsed.netloc,
            "title": title,
            "text": text,
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "url": url,
            "domain": urlparse(url).netloc,
            "title": "",
            "text": "",
            "error": f"Network or HTTP error: {e}",
        }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "domain": urlparse(url).netloc,
            "title": "",
            "text": "",
            "error": f"Unexpected parse error: {e}",
        }
