from pathlib import Path

import spacy
from tqdm import tqdm

from config import CORPUS, FULL, PROBLEM


def read_corpus(f: Path) -> list[str]:
    data = []
    with f.open(mode="r", encoding="utf-8") as file:
        current_str = ""
        for line in tqdm(file):
            if line == "\n":
                data.append(current_str)
                current_str = ""
            else:
                line = line.replace("\n", " ")
                current_str += line
    return data


def process(f: Path) -> None:
    nlp = spacy.load("pl_core_news_sm", disable=["parser", "ner"])
    restricted_words = {"@user", "@anonymized_account", " ", "rt"}

    corpus = read_corpus(f)

    output_file = Path(f"{f.stem}_analysis.csv")

    with output_file.open(mode="w", encoding="utf-8") as output:
        output.write("Text,POS")

        for text in tqdm(corpus):
            output.write("\n")

            doc = nlp(text)

            output.write(
                "\n".join(
                    f"{token.lemma_.lower()},{token.pos_}"
                    for token in doc
                    if not (
                        token.is_stop
                        or token.is_punct
                        or token.like_num
                        or token.is_digit
                        or token.lemma_.lower() in restricted_words
                    )
                )
            )


def main():
    process(FULL)
    process(CORPUS)
    process(PROBLEM)


if __name__ == "__main__":
    main()
