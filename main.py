#!/usr/bin/env python3
"""
main.py — CLI interface for the AI Text Summarizer Tool
Usage:
    python main.py --text "Your text here"
    python main.py --file samples/article.txt --style detailed --bullets
"""

import argparse
import sys
from summarizer import summarize, summarize_file


def print_result(result: dict):
    print("\n" + "=" * 60)
    print(f"  SUMMARY  [style: {result['style']} | ~{result['word_count']} words]")
    print("=" * 60)
    print(result["summary"])
    if result["keywords"]:
        print("\n🔑 Keywords: " + ", ".join(result["keywords"]))
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="🧠 AI-Powered Text Summarizer using Claude",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", type=str, help="Text string to summarize")
    group.add_argument("--file", type=str, help="Path to a .txt file to summarize")

    parser.add_argument(
        "--style",
        choices=["concise", "detailed", "eli5"],
        default="concise",
        help="Summary style:\n  concise  — short and to the point (default)\n  detailed — full coverage\n  eli5     — simple language",
    )
    parser.add_argument(
        "--bullets",
        action="store_true",
        help="Output summary as bullet points",
    )
    parser.add_argument(
        "--max-words",
        type=int,
        default=150,
        help="Approximate max word count for the summary (default: 150)",
    )

    args = parser.parse_args()

    print("\n⏳ Summarizing...")

    try:
        if args.text:
            result = summarize(
                text=args.text,
                style=args.style,
                bullet_points=args.bullets,
                max_words=args.max_words,
            )
        else:
            result = summarize_file(
                filepath=args.file,
                style=args.style,
                bullet_points=args.bullets,
                max_words=args.max_words,
            )
        print_result(result)

    except FileNotFoundError:
        print(f"\n❌ Error: File '{args.file}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
