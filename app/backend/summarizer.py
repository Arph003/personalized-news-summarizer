# app/backend/summarizer.py

from transformers import pipeline
from typing import Optional


# 为了第一次加载不会太慢，也避免每次调用都重新加载模型
# 这里用一个全局的 lazy 初始化
_summarizer_pipeline = None


def get_summarizer():
    """
    Lazy load summarization pipeline.
    可以根据需要换模型：
    - "t5-small"
    - "google/pegasus-xsum"
    """
    global _summarizer_pipeline
    if _summarizer_pipeline is None:
        # 模型尽量选小一点的，避免本地太卡
        _summarizer_pipeline = pipeline(
            "summarization",
            model="t5-small",          # 初版先用 t5-small，够用而且轻量
            tokenizer="t5-small"
        )
    return _summarizer_pipeline


def summarize_text(
    text: str,
    max_length: int = 130,
    min_length: int = 30,
    do_sample: bool = False
) -> Optional[str]:
    """
    输入一段新闻正文文本，返回一段英文摘要。
    如果文本太长，会自动截断到合适长度。
    """
    if not text or not text.strip():
        return ""

    # 保险起见，太长的直接截到前 4000 个字符，避免超最大长度
    text = text.strip()
    if len(text) > 4000:
        text = text[:4000]

    summarizer = get_summarizer()
    try:
        result = summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=do_sample,
            truncation=True,
        )
        if not result:
            return ""
        # t5-small 输出在 'summary_text' 字段
        return result[0]["summary_text"]
    except Exception as e:
        # 为了稳一点，出错时返回 None 或空字符串都可以
        print(f"[summarizer] Error during summarization: {e}")
        return ""
