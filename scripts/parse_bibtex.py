#!/usr/bin/env python3
"""
Parse BibTeX file and convert to JSON for Hugo.
Usage: uv run python scripts/parse_bibtex.py
"""

import json
import re
import sys
from pathlib import Path

import bibtexparser


def clean_latex(text: str) -> str:
    """Remove LaTeX formatting from text."""
    if not text:
        return ""
    # Remove braces
    text = text.replace("{", "").replace("}", "")
    # Handle common LaTeX accents
    replacements = {
        "\\'a": "á",
        "\\'e": "é",
        "\\'i": "í",
        "\\'o": "ó",
        "\\'u": "ú",
        "\\'c": "ć",
        "\\v{c}": "č",
        "\\v{s}": "š",
        "\\v{z}": "ž",
        "\\v{S}": "Š",
        "\\v{Z}": "Ž",
        "\\v{C}": "Č",
        '\\"o': "ö",
        '\\"u': "ü",
        '\\"a': "ä",
        "\\~n": "ñ",
        "\\c{c}": "ç",
    }
    for latex, char in replacements.items():
        text = text.replace(latex, char)
    # Remove remaining backslashes before letters
    text = re.sub(r"\\([a-zA-Z])", r"\1", text)
    return text.strip()


def parse_authors(author_str: str) -> list[str]:
    """Parse author string into list of names."""
    if not author_str:
        return []
    authors = author_str.split(" and ")
    result = []
    for author in authors:
        author = clean_latex(author.strip())
        # Handle "Last, First" format
        if "," in author:
            parts = author.split(",", 1)
            author = f"{parts[1].strip()} {parts[0].strip()}"
        result.append(author)
    return result


def parse_bibtex(bib_path: str, output_path: str) -> None:
    """Parse BibTeX file and write JSON output."""
    with open(bib_path) as f:
        bib_db = bibtexparser.load(f)

    publications = []
    seen_titles = set()  # Deduplicate by title

    for entry in bib_db.entries:
        title = clean_latex(entry.get("title", ""))

        # Skip duplicates
        title_lower = title.lower()
        if title_lower in seen_titles:
            continue
        seen_titles.add(title_lower)

        pub = {
            "key": entry.get("ID", ""),
            "type": entry.get("ENTRYTYPE", ""),
            "title": title,
            "year": entry.get("year", ""),
            "authors": parse_authors(entry.get("author", "")),
            "venue": "",
            "links": {},
        }

        # Determine venue
        if entry.get("journal"):
            pub["venue"] = clean_latex(entry["journal"])
        elif entry.get("booktitle"):
            pub["venue"] = clean_latex(entry["booktitle"])
        elif entry.get("school"):
            pub["venue"] = clean_latex(entry["school"])
        elif entry.get("publisher"):
            pub["venue"] = clean_latex(entry["publisher"])

        # Extract links
        if entry.get("url"):
            pub["links"]["url"] = entry["url"]
        if entry.get("doi"):
            doi = entry["doi"]
            pub["links"]["doi"] = (
                f"https://doi.org/{doi}" if not doi.startswith("http") else doi
            )

        # Check for arXiv
        if (
            "arxiv" in pub["venue"].lower()
            or "arxiv" in entry.get("journal", "").lower()
        ):
            # Extract arXiv ID from journal field
            arxiv_match = re.search(r"arXiv[:\s]*(\d+\.\d+)", entry.get("journal", ""))
            if arxiv_match:
                pub["links"]["arxiv"] = f"https://arxiv.org/abs/{arxiv_match.group(1)}"

        # Volume/pages for journals
        if entry.get("volume"):
            pub["volume"] = entry["volume"]
        if entry.get("pages"):
            pub["pages"] = entry["pages"]

        publications.append(pub)

    # Sort by year (newest first)
    publications.sort(key=lambda x: x.get("year", "0"), reverse=True)

    # Write JSON
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(publications, f, indent=2, ensure_ascii=False)

    print(f"Parsed {len(publications)} publications to {output_path}")


if __name__ == "__main__":
    bib_file = "bibtex/publications.bib"
    json_file = "data/publications.json"

    if len(sys.argv) > 1:
        bib_file = sys.argv[1]
    if len(sys.argv) > 2:
        json_file = sys.argv[2]

    if not Path(bib_file).exists():
        print(f"Warning: {bib_file} not found. Creating empty publications.json")
        Path(json_file).parent.mkdir(parents=True, exist_ok=True)
        with open(json_file, "w") as f:
            json.dump([], f)
    else:
        parse_bibtex(bib_file, json_file)
