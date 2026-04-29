"""
LangChain-powered summarizer using Claude API
"""

from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)
import os


STYLE_PROMPTS = {
    "concise": "Provide a brief, concise summary in 2-3 sentences capturing only the most essential points.",
    "detailed": "Provide a detailed, comprehensive summary covering all key points, arguments, and supporting details.",
    "eli5": "Explain this in very simple terms as if explaining to a 5-year-old or someone with no background knowledge."
}


def get_llm(api_key: str):
    """Initialize Claude via LangChain"""
    return ChatAnthropic(
        model="claude-opus-4-5",
        anthropic_api_key=api_key,
        max_tokens=1024
    )


def summarize_with_langchain(text: str, style: str, bullet_points: bool,
                              extract_keywords: bool, api_key: str) -> dict:
    """
    Summarize text using LangChain + Claude.
    Handles long texts by splitting into chunks automatically.
    """
    llm = get_llm(api_key)

    # Split text into manageable chunks (LangChain feature)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=3000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    # Build dynamic prompt using LangChain PromptTemplate
    format_instruction = "Format as bullet points." if bullet_points else "Format as flowing paragraphs."
    keyword_instruction = "\n\nAfter the summary, add 'KEYWORDS:' followed by 5-8 important keywords separated by commas." if extract_keywords else ""

    map_prompt_template = PromptTemplate(
        input_variables=["text"],
        template=f"""Summarize the following text chunk.
Style: {STYLE_PROMPTS.get(style, STYLE_PROMPTS['concise'])}
{format_instruction}

TEXT:
{{text}}

SUMMARY:"""
    )

    combine_prompt_template = PromptTemplate(
        input_variables=["text"],
        template=f"""You are given multiple summaries of chunks from a larger text.
Combine them into one cohesive final summary.
Style: {STYLE_PROMPTS.get(style, STYLE_PROMPTS['concise'])}
{format_instruction}{keyword_instruction}

SUMMARIES:
{{text}}

FINAL SUMMARY:"""
    )

    # Use LangChain's map_reduce chain for long documents
    if len(docs) > 1:
        chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            map_prompt=map_prompt_template,
            combine_prompt=combine_prompt_template,
            verbose=False
        )
    else:
        chain = load_summarize_chain(
            llm,
            chain_type="stuff",
            prompt=combine_prompt_template,
            verbose=False
        )

    result = chain.invoke({"input_documents": docs})
    output = result.get("output_text", "")

    # Parse keywords if extracted
    summary = output
    keywords = []
    if extract_keywords and "KEYWORDS:" in output:
        parts = output.split("KEYWORDS:")
        summary = parts[0].strip()
        keywords = [k.strip() for k in parts[1].strip().split(",") if k.strip()]

    return {
        "summary": summary,
        "keywords": keywords,
        "chunks_processed": len(docs)
    }


def create_conversation_chain(api_key: str):
    """
    Create a conversational chain with memory using LangChain.
    Allows follow-up questions about the summarized text.
    """
    llm = get_llm(api_key)

    memory = ConversationBufferMemory(return_messages=True)

    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(
            "You are a helpful AI assistant that helps users understand and analyze text. "
            "You have memory of the conversation and can answer follow-up questions."
        ),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    conversation = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=False
    )

    return conversation
