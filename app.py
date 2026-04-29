import streamlit as st
import os
from langchain_summarizer import summarize_with_langchain, create_conversation_chain

# Page config
st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

h1 {
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 2rem;
}

.stTextArea textarea {
    background-color: #1e1b4b !important;
    color: #e2e8f0 !important;
    border: 1px solid #4338ca !important;
    border-radius: 12px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.9rem !important;
}

.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    width: 100% !important;
}

.result-box {
    background: linear-gradient(135deg, #1e1b4b, #172554);
    border: 1px solid #4338ca;
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #e2e8f0;
    line-height: 1.8;
    font-size: 0.95rem;
}

.keyword-tag {
    display: inline-block;
    background: linear-gradient(90deg, #7c3aed33, #2563eb33);
    border: 1px solid #7c3aed;
    color: #a78bfa;
    border-radius: 20px;
    padding: 3px 14px;
    margin: 4px;
    font-size: 0.82rem;
    font-weight: 600;
}

.section-label {
    color: #7c3aed;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.stat-card {
    background: #1e1b4b;
    border: 1px solid #4338ca;
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    text-align: center;
}

.stat-number {
    font-size: 1.5rem;
    font-weight: 700;
    color: #a78bfa;
}

.stat-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.chat-msg-user {
    background: #1e1b4b;
    border-left: 3px solid #7c3aed;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    color: #e2e8f0;
}

.chat-msg-ai {
    background: #172554;
    border-left: 3px solid #2563eb;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    color: #e2e8f0;
}

.badge {
    display: inline-block;
    background: #7c3aed22;
    border: 1px solid #7c3aed;
    color: #a78bfa;
    border-radius: 6px;
    padding: 2px 10px;
    font-size: 0.75rem;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>🧠 AI Text Summarizer</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by <b>Claude API</b> + <b>LangChain</b> · Smart Summaries with Memory</p>', unsafe_allow_html=True)

# Tech badges
st.markdown("""
<div style="text-align:center; margin-bottom:1.5rem;">
    <span class="badge">🤖 Claude API</span>
    <span class="badge">🦜 LangChain</span>
    <span class="badge">🐍 Python</span>
    <span class="badge">✨ Streamlit</span>
</div>
""", unsafe_allow_html=True)

# Session state init
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "summary_done" not in st.session_state:
    st.session_state.summary_done = False

# API Key
api_key = st.text_input("🔑 Anthropic API Key", type="password", placeholder="sk-ant-...", help="Your Anthropic API key")

# Tabs
tab1, tab2 = st.tabs(["📝 Summarize", "💬 Ask Follow-up Questions"])

with tab1:
    st.markdown('<p class="section-label">Input Text</p>', unsafe_allow_html=True)
    input_text = st.text_area("", height=200, placeholder="Paste any text here — articles, essays, reports, emails...")

    # Stats
    if input_text:
        words = len(input_text.split())
        chars = len(input_text)
        sentences = input_text.count('.') + input_text.count('!') + input_text.count('?')
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{words}</div><div class="stat-label">Words</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{chars}</div><div class="stat-label">Characters</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{sentences}</div><div class="stat-label">Sentences</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        style = st.selectbox("🎨 Summary Style", ["concise", "detailed", "eli5"],
                             format_func=lambda x: {"concise": "⚡ Concise", "detailed": "📋 Detailed", "eli5": "🧒 ELI5"}[x])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        bullet_points = st.checkbox("🔸 Bullet Point Format")
        extract_keywords = st.checkbox("🏷️ Extract Keywords", value=True)

    if st.button("✨ Summarize with LangChain + Claude"):
        if not api_key:
            st.error("⚠️ Please enter your Anthropic API key.")
        elif not input_text.strip():
            st.error("⚠️ Please enter some text to summarize.")
        else:
            with st.spinner("🦜 LangChain + Claude is processing..."):
                try:
                    result = summarize_with_langchain(
                        input_text, style, bullet_points, extract_keywords, api_key
                    )

                    st.markdown('<p class="section-label">📄 Summary</p>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box">{result["summary"]}</div>', unsafe_allow_html=True)

                    if result["keywords"]:
                        st.markdown('<br><p class="section-label">🏷️ Keywords</p>', unsafe_allow_html=True)
                        tags_html = "".join([f'<span class="keyword-tag">{kw}</span>' for kw in result["keywords"]])
                        st.markdown(f'<div>{tags_html}</div>', unsafe_allow_html=True)

                    if result["chunks_processed"] > 1:
                        st.info(f"📚 Long document detected — processed in {result['chunks_processed']} chunks using LangChain!")

                    # Save context for chat
                    st.session_state.summary_done = True
                    st.session_state.conversation = create_conversation_chain(api_key)
                    # Prime the conversation with the text
                    st.session_state.conversation.predict(
                        input=f"Here is a text I want to discuss: {input_text[:2000]}... The summary is: {result['summary']}"
                    )
                    st.session_state.chat_history = []
                    st.success("✅ Done! Go to '💬 Ask Follow-up Questions' tab to chat about this text!")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

with tab2:
    if not st.session_state.summary_done:
        st.info("👆 First summarize a text in the Summarize tab, then come here to ask questions about it!")
    else:
        st.markdown("**Ask anything about the text you just summarized!**")
        st.markdown("*LangChain's memory keeps track of the whole conversation* 🧠")

        # Chat history display
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-msg-user">👤 <b>You:</b> {msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-msg-ai">🤖 <b>Claude:</b> {msg["content"]}</div>', unsafe_allow_html=True)

        user_question = st.text_input("Your question:", placeholder="e.g. What is the main argument? Can you explain more?")

        if st.button("💬 Ask"):
            if user_question.strip():
                with st.spinner("🤔 Thinking..."):
                    try:
                        response = st.session_state.conversation.predict(input=user_question)
                        st.session_state.chat_history.append({"role": "user", "content": user_question})
                        st.session_state.chat_history.append({"role": "ai", "content": response})
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown('<p style="text-align:center; color:#475569; font-size:0.8rem;">Built with ❤️ using Claude API + LangChain + Streamlit · github.com/lsheeta7/text-summarizer-tool</p>', unsafe_allow_html=True)
