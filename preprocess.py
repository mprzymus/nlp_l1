import typing as t
from pathlib import Path

import pandas as pd
from langdetect import LangDetectException, detect
from tqdm import tqdm

CORPUS_DIR = Path("scraped")
OUTPUT_DIR = Path("clean")
OUTPUT_DIR.mkdir(exist_ok=True)


def clean_text(text: str) -> t.Optional[str]:
    text = text.strip()

    try:
        lang = detect(text)
    except LangDetectException:
        lang = None

    if lang != "pl":
        return None

    return text


def preprocess_file(f: Path) -> None:
    df = pd.read_json(f, lines=True)

    for _, data in df.iterrows():
        content = data["content"]

        cleaned = clean_text(content)

        if cleaned:
            output_file = OUTPUT_DIR / f"{data['id']}.txt"
            output_file.write_text(cleaned, encoding="utf-8")


def main() -> None:
    files = list(CORPUS_DIR.rglob("*.jsonl"))
    for f in tqdm(files):
        preprocess_file(f)


if __name__ == "__main__":
    main()
