# 🧠 AI Text Summarizer Tool

A Python CLI tool that uses the **Claude API (Anthropic)** to intelligently summarize any text or `.txt` file. Supports multiple summary styles, bullet-point formatting, and automatic keyword extraction.

---

## ✨ Features

- 📝 Summarize raw text or `.txt` files from the command line
- 🎨 Three summary styles: `concise`, `detailed`, `eli5`
- 🔘 Optional bullet-point output
- 🔑 Auto keyword extraction from input text
- ⚙️ Configurable max word count
- ✅ Unit-tested with `pytest` and mock API support

---

## 📁 Project Structure

```
text-summarizer-tool/
│
├── main.py                  # CLI entry point
├── requirements.txt         # Dependencies
├── .env.example             # API key template
├── .gitignore
│
├── summarizer/
│   ├── __init__.py
│   └── core.py              # Core summarization logic (Claude API)
│
├── samples/
│   └── article.txt          # Sample text file for testing
│
└── tests/
    └── test_summarizer.py   # Unit tests (pytest)
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/text-summarizer-tool.git
cd text-summarizer-tool
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your API key

```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

Or export it directly:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key at [console.anthropic.com](https://console.anthropic.com).

---

## 🖥️ Usage

### Summarize a text string

```bash
python main.py --text "Artificial intelligence is reshaping the world by automating tasks and enabling smarter decisions across industries."
```

### Summarize a file

```bash
python main.py --file samples/article.txt
```

### Use detailed style with bullet points

```bash
python main.py --file samples/article.txt --style detailed --bullets
```

### Explain like I'm 5 (ELI5)

```bash
python main.py --text "Quantum computing uses quantum bits..." --style eli5
```

### Limit summary length

```bash
python main.py --file samples/article.txt --max-words 80
```

---

## ⚙️ CLI Arguments

| Argument | Description | Default |
|---|---|---|
| `--text` | Raw text string to summarize | — |
| `--file` | Path to a `.txt` file | — |
| `--style` | `concise` / `detailed` / `eli5` | `concise` |
| `--bullets` | Output as bullet points | `False` |
| `--max-words` | Approx. max words in summary | `150` |

---

## 🧪 Running Tests

```bash
pytest tests/
```

Tests use mocked API responses so no real API calls are made during testing.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Anthropic Claude API** (`claude-opus-4-5`)
- **argparse** — CLI argument parsing
- **pytest** — Unit testing

---

## 📄 License

MIT License. Feel free to use and modify.

---

## 🙋 Author

Built with ❤️ using the Anthropic Claude API.
