from argparse import ArgumentParser, Namespace
from itertools import count
from multiprocessing import Manager, Pool, Process, Queue
from pathlib import Path
from queue import Empty

from tqdm import tqdm
from ufal.morphodita import Forms, TaggedLemmas, Tagger, TokenRanges

from config import (
    CORPUS,
    CORPUS_ANALYSIS,
    FULL,
    FULL_ANALYSIS,
    MORPHODITA_TAGGER,
    PROBLEM,
    PROBLEM_ANALYSIS,
    STOPWORDS,
    ensure_morphodita_tagger,
)


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


def process(read_queue: Queue, write_queue: Queue) -> None:
    stopwords = STOPWORDS.read_text(encoding="utf-8").split()
    restricted_words = {"@user", "@anonymized_account", " ", "rt", *stopwords}
    restricted_pos = {"C", "Z"}

    tagger = Tagger.load(str(MORPHODITA_TAGGER))
    tokenizer = tagger.newTokenizer()
    forms = Forms()
    lemmas = TaggedLemmas()
    tokens = TokenRanges()

    while not read_queue.empty():
        try:
            text = read_queue.get(block=False, timeout=0.1)
        except Empty:
            continue

        tokenizer.setText(text.strip())
        while tokenizer.nextSentence(forms, tokens):
            tagger.tag(forms, lemmas)

            for lemma in lemmas:
                normalized_lemma = lemma.lemma.lower()
                pos = lemma.tag[0]

                if not (
                    normalized_lemma.isnumeric()
                    or pos in restricted_pos
                    or normalized_lemma in restricted_words
                ):
                    write_queue.put(f"{normalized_lemma},{pos}\n")


def write_output(from_: Queue, to: Path) -> None:
    with to.open(mode="w", encoding="utf-8") as output:
        output.write("Text,POS\n")

        for _ in tqdm(count()):
            data = from_.get()

            if data is None:
                break

            output.write(data)


def process_multiprocessing(f: Path, output_file: Path, processes: int) -> None:
    with Manager() as manager:
        read_queue = manager.Queue()
        write_queue = manager.Queue(maxsize=500_000)

        for text in read_corpus(f):
            read_queue.put(text)

        write_process = Process(target=write_output, args=(write_queue, output_file))
        write_process.start()

        with Pool(processes) as pool:
            for _ in range(processes):
                pool.apply_async(process, (read_queue, write_queue))

            pool.close()
            pool.join()

        write_queue.put(None)
        write_process.join()


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-p", "--processes", type=int, default=20)
    return parser.parse_args()


def main():
    args = parse_args()
    ensure_morphodita_tagger()

    process_multiprocessing(FULL, FULL_ANALYSIS, args.processes)
    process_multiprocessing(CORPUS, CORPUS_ANALYSIS, args.processes)
    process_multiprocessing(PROBLEM, PROBLEM_ANALYSIS, args.processes)


if __name__ == "__main__":
    main()
