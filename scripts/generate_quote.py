from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
QUOTE_FILE = DOCS_DIR / "latest-quote.json"
HISTORY_FILE = ROOT / "quotes-history.md"
INDEX_FILE = DOCS_DIR / "index.html"
INDEX_DATA_MARKER = "window.__QUOTE_DATA__ = "

QUOTES = [
    {
        "text": "Start where you are. Use what you have. Do what you can.",
        "author": "Arthur Ashe",
    },
    {
        "text": "Success is the sum of small efforts, repeated day in and day out.",
        "author": "Robert Collier",
    },
    {
        "text": "It always seems impossible until it is done.",
        "author": "Nelson Mandela",
    },
    {
        "text": "The future depends on what you do today.",
        "author": "Mahatma Gandhi",
    },
    {
        "text": "Do not wait to strike till the iron is hot; but make it hot by striking.",
        "author": "William Butler Yeats",
    },
    {
        "text": "Dream big and dare to fail.",
        "author": "Norman Vaughan",
    },
    {
        "text": "Small deeds done are better than great deeds planned.",
        "author": "Peter Marshall",
    },
]


def choose_quote() -> dict[str, str]:
    day_number = datetime.now(UTC).timetuple().tm_yday
    return QUOTES[(day_number - 1) % len(QUOTES)]


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
    marker_start = content.find(INDEX_DATA_MARKER)
    if marker_start == -1:
        raise ValueError("Quote data marker not found in docs/index.html")

    json_start = marker_start + len(INDEX_DATA_MARKER)
    json_end = content.find(";", json_start)
    if json_end == -1:
        raise ValueError("Quote data marker is missing a closing semicolon")

    embedded_data = json.dumps(payload, indent=8)
    updated = f"{content[:json_start]}{embedded_data}{content[json_end:]}"
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
