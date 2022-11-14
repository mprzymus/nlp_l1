from pathlib import Path

import pandas as pd
import spacy
from tqdm import tqdm

FULL_FILE = Path("full.txt")
CORPUS_FILE = Path("corpus.txt")
PROBLEM_FILE = Path("problem.txt")


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
    nlp = spacy.load("pl_core_news_sm", disable=["parser", "ner", "tok2vec"])
    restricted_words = {"@user", "@anonymized_account", " ", "rt"}

    analyzed: list[tuple[str, str]] = []
    corpus = read_corpus(f)

    for text in tqdm(corpus):
        doc = nlp(text)

        analyzed.extend(
            (token.lemma_.lower(), token.pos_)
            for token in doc
            if not (
                token.is_stop
                or token.is_punct
                or token.like_num
                or token.is_digit
                or token.lemma_.lower() in restricted_words
            )
        )

    output = pd.DataFrame(analyzed, columns=["Text", "POS"])
    output.to_csv(f"{f.stem}_analysis.csv", index=False)


def main():
    process(FULL_FILE)
    process(CORPUS_FILE)
    process(PROBLEM_FILE)


if __name__ == "__main__":
    main()
