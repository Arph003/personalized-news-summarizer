from app.backend.scraper import fetch_article
from app.backend.summarizer import summarize_text

url = "https://www.ibm.com/think/topics/foundation-models"

result = fetch_article(url)

if result["success"]:
    article_text = result["text"]
    print("\n=== 原文前 400 字 ===\n")
    print(article_text[:400])

    summary = summarize_text(article_text)
    print("\n=== 摘要 ===\n")
    print(summary)
else:
    print("抓取失败，错误信息：", result.get("error"))
