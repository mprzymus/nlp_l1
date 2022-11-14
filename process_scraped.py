import typing as t
from pathlib import Path

import pandas as pd
from langdetect import LangDetectException, detect
from tqdm import tqdm

from config import CONTENT_LINK_REGEX, CORPUS, SCRAPED_DIR, USER_REGEX


def clean_text(text: str) -> t.Optional[str]:
    text = CONTENT_LINK_REGEX.sub("", text)
    text = USER_REGEX.sub("@user", text)
    text = text.replace("  ", " ").replace("\n\n", "\n").strip()

    try:
        lang = detect(text)
    except LangDetectException:
        lang = None

    if lang != "pl":
        return None

    return text


def preprocess_file(f: Path) -> None:
    df = pd.read_json(f, lines=True)

    with CORPUS.open("a", encoding="utf-8") as output:
        for _, data in df.iterrows():
            content = data["content"]
            cleaned = clean_text(content)

            if cleaned:
                output.write(cleaned)
                output.write("\n\n")


def main() -> None:
    files = list(SCRAPED_DIR.rglob("*.jsonl"))
    for f in tqdm(files):
        preprocess_file(f)


if __name__ == "__main__":
    main()
