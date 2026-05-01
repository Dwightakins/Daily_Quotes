from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
QUOTE_FILE = DOCS_DIR / "latest-quote.json"
HISTORY_FILE = ROOT / "quotes-history.md"
INDEX_FILE = DOCS_DIR / "index.html"
INDEX_DATA_START_MARKER = "/* QUOTE_DATA_START */"
INDEX_DATA_END_MARKER = "/* QUOTE_DATA_END */"
ZENQUOTES_TODAY_URL = "https://zenquotes.io/api/today"

FALLBACK_QUOTE = {
    "text": "Start where you are. Use what you have. Do what you can.",
    "author": "Arthur Ashe",
    "source": "Local fallback",
}


def choose_quote() -> dict[str, str]:
    try:
        with urlopen(ZENQUOTES_TODAY_URL, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        if not data or not isinstance(data, list):
            raise ValueError("Unexpected response from ZenQuotes")

        quote = data[0]
        return {
            "text": quote["q"],
            "author": quote["a"],
            "source": "ZenQuotes",
        }
    except (URLError, TimeoutError, ValueError, KeyError, json.JSONDecodeError):
        return FALLBACK_QUOTE


def build_history_entry(timestamp: str, quote: dict[str, str]) -> str:
    return f'- {timestamp}: "{quote["text"]}" - {quote["author"]}'


def create_history_file(entry: str) -> str:
    return "\n".join(
        [
            "# Quote History",
            "",
            "This file stores the quotes chosen by the GitHub automation.",
            "",
            "## Daily Quotes",
            entry,
            "",
        ]
    )


def update_index_file(payload: dict[str, str]) -> None:
    content = INDEX_FILE.read_text(encoding="utf-8")
    marker_start = content.find(INDEX_DATA_START_MARKER)
    marker_end = content.find(INDEX_DATA_END_MARKER)
    if marker_start == -1 or marker_end == -1 or marker_end <= marker_start:
        raise ValueError("Quote data markers not found in docs/index.html")

    data_start = marker_start + len(INDEX_DATA_START_MARKER)
    embedded_data = "\n" + json.dumps(payload, indent=8) + "\n      "
    updated = f"{content[:data_start]}{embedded_data}{content[marker_end:]}"
    INDEX_FILE.write_text(updated, encoding="utf-8")


def main() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(UTC)
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    quote = choose_quote()

    payload = {
        "date": now.strftime("%Y-%m-%d"),
        "updated_at": timestamp,
        "quote": quote["text"],
        "author": quote["author"],
        "source": quote["source"],
    }
    QUOTE_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    update_index_file(payload)

    entry = build_history_entry(timestamp, quote)
    if HISTORY_FILE.exists():
        existing = HISTORY_FILE.read_text(encoding="utf-8").rstrip()
        HISTORY_FILE.write_text(f"{existing}\n{entry}\n", encoding="utf-8")
    else:
        HISTORY_FILE.write_text(create_history_file(entry), encoding="utf-8")

    print(f"Wrote {QUOTE_FILE}")
    print(f"Updated {HISTORY_FILE}")


if __name__ == "__main__":
    main()
