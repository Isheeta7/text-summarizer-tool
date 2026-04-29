"""
core.py — Text Summarizer core logic using Claude API (Anthropic)
"""

import anthropic
import re


def summarize(
    text: str,
    style: str = "concise",
    bullet_points: bool = False,
    max_words: int = 150,
) -> dict:
    """
    Summarize the provided text using Claude.

    Args:
        text         : Input text to summarize.
        style        : 'concise', 'detailed', or 'eli5' (explain like I'm 5).
        bullet_points: If True, return summary as bullet points.
        max_words    : Approximate maximum word count for the summary.

    Returns:
        A dict with keys: summary, word_count, style, keywords
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    style_instructions = {
        "concise": "Provide a clear and concise summary.",
        "detailed": "Provide a detailed summary covering all key points.",
        "eli5": "Explain this in very simple language as if explaining to a 5-year-old.",
    }

    if style not in style_instructions:
        raise ValueError(f"Style must be one of: {list(style_instructions.keys())}")

    format_instruction = (
        "Format the summary as bullet points." if bullet_points else "Write in paragraph form."
    )

    prompt = f"""You are an expert text summarizer.

Task: Summarize the following text.
Style: {style_instructions[style]}
Format: {format_instruction}
Length: Keep it under {max_words} words.

Also extract 5 important keywords from the text.

Respond ONLY in this exact format:
SUMMARY:
<your summary here>

KEYWORDS:
<comma-separated keywords>

Text to summarize:
\"\"\"
{text}
\"\"\"
"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()

    # Parse response
    summary_match = re.search(r"SUMMARY:\s*(.*?)\s*KEYWORDS:", raw, re.DOTALL)
    keywords_match = re.search(r"KEYWORDS:\s*(.*)", raw, re.DOTALL)

    summary_text = summary_match.group(1).strip() if summary_match else raw
    keywords_raw = keywords_match.group(1).strip() if keywords_match else ""
    keywords = [kw.strip() for kw in keywords_raw.split(",") if kw.strip()]

    return {
        "summary": summary_text,
        "word_count": len(summary_text.split()),
        "style": style,
        "keywords": keywords,
    }


def summarize_file(filepath: str, **kwargs) -> dict:
    """Read a .txt file and summarize its contents."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return summarize(text, **kwargs)
