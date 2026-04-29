"""
tests/test_summarizer.py — Unit tests for the Text Summarizer Tool
Run with: pytest tests/
"""

import pytest
from unittest.mock import patch, MagicMock
from summarizer.core import summarize


SAMPLE_TEXT = """
Artificial intelligence is transforming the world. 
From healthcare to education, AI tools are improving lives 
and reshaping industries. However, it also raises ethical 
questions around privacy, bias, and employment.
"""

MOCK_API_RESPONSE = """SUMMARY:
AI is transforming multiple sectors including healthcare and education, 
while raising ethical concerns about privacy, bias, and job displacement.

KEYWORDS:
artificial intelligence, healthcare, education, ethics, bias
"""


def make_mock_client(response_text):
    mock_content = MagicMock()
    mock_content.text = response_text

    mock_message = MagicMock()
    mock_message.content = [mock_content]

    mock_messages = MagicMock()
    mock_messages.create.return_value = mock_message

    mock_client = MagicMock()
    mock_client.messages = mock_messages
    return mock_client


@patch("summarizer.core.anthropic.Anthropic")
def test_summarize_returns_dict(mock_anthropic):
    mock_anthropic.return_value = make_mock_client(MOCK_API_RESPONSE)
    result = summarize(SAMPLE_TEXT)
    assert isinstance(result, dict)
    assert "summary" in result
    assert "keywords" in result
    assert "word_count" in result
    assert "style" in result


@patch("summarizer.core.anthropic.Anthropic")
def test_summarize_default_style(mock_anthropic):
    mock_anthropic.return_value = make_mock_client(MOCK_API_RESPONSE)
    result = summarize(SAMPLE_TEXT)
    assert result["style"] == "concise"


@patch("summarizer.core.anthropic.Anthropic")
def test_summarize_detailed_style(mock_anthropic):
    mock_anthropic.return_value = make_mock_client(MOCK_API_RESPONSE)
    result = summarize(SAMPLE_TEXT, style="detailed")
    assert result["style"] == "detailed"


@patch("summarizer.core.anthropic.Anthropic")
def test_keywords_are_list(mock_anthropic):
    mock_anthropic.return_value = make_mock_client(MOCK_API_RESPONSE)
    result = summarize(SAMPLE_TEXT)
    assert isinstance(result["keywords"], list)
    assert len(result["keywords"]) > 0


def test_empty_text_raises_error():
    with pytest.raises(ValueError):
        summarize("")


def test_whitespace_text_raises_error():
    with pytest.raises(ValueError):
        summarize("   ")


def test_invalid_style_raises_error():
    with pytest.raises(ValueError):
        summarize(SAMPLE_TEXT, style="invalid_style")
