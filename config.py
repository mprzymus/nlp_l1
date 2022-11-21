import re
import urllib.request
from pathlib import Path

import pandas as pd

START = "2019-07-01"
END = "2022-11-12"

NKJP_DIR = Path("nkjp")
EXTRAS_DIR = Path("extras")

SCRAPED_DIR = Path("scraped")
OUTPUTS_DIR = Path("outputs")
SCRAPED_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)

SCRAPED_DONE = SCRAPED_DIR / "done.json"

NKJP = OUTPUTS_DIR / "nkjp.txt"
OSCAR = OUTPUTS_DIR / "oscar.txt"

FULL = OUTPUTS_DIR / "full.txt"
CORPUS = OUTPUTS_DIR / "corpus.txt"
PROBLEM = OUTPUTS_DIR / "problem.txt"

FULL_ANALYSIS = OUTPUTS_DIR / "full_analysis.csv"
CORPUS_ANALYSIS = OUTPUTS_DIR / "corpus_analysis.csv"
PROBLEM_ANALYSIS = OUTPUTS_DIR / "problem_analysis.csv"

STOPWORDS = EXTRAS_DIR / "stopwords.txt"
MORPHODITA_TAGGER = EXTRAS_DIR / "pl.tagger"

CONTENT_LINK_REGEX = re.compile(r"https?://t.co/[a-zA-Z0-9]+")
USER_REGEX = re.compile(r"(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)")

PL_TAGGER_URL = "https://clarin-pl.eu/dspace/bitstream/handle/11321/425/pl.tagger"


def date_range():
    dates = [d.to_pydatetime().date() for d in pd.date_range(START, END).to_list()]
    dates.reverse()
    return dates


def ensure_morphodita_tagger():
    if not MORPHODITA_TAGGER.is_file():
        print(f"Morphodita pl.tagger not found, downloading from {PL_TAGGER_URL}...")
        urllib.request.urlretrieve(PL_TAGGER_URL, MORPHODITA_TAGGER)
