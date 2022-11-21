# NLP Laboratorium 1

## Autorzy

* Tomasz Dróżdż
* Marcin Przymus

## Do uruchomienia

```bash
pip install -r requirements.txt
```

Korpus milionowy NKJP należy wypakować do katalogu `nkjp`:

```bash
.
├── analyze_morphology.py
├── ...
├── nkjp
│   ├── 010-2-000000001
│   │   ├── ann_groups.xml
│   │   ├── ann_morphosyntax.xml
│   │   ├── ann_named.xml
│   │   ├── ann_segmentation.xml
│   │   ├── ann_senses.xml
│   │   ├── ann_words.xml
│   │   ├── header.xml
│   │   └── text.xml
│   ├── 030-2-000000001
│   │   ├── ann_groups.xml
│   │   ├── ann_morphosyntax.xml
|   |   ├── ...
```

Korpus Oscar należy pobrać z [tego repozytorium](https://github.com/Ermlab/PoLitBert#:~:text=zip%20(0.58%20GB)-,Cleaned%20Polish%20Oscar%20corpus,-corpus_oscar_2020%2D04%2D10_32M_lines)
i wypakować plik tekstowy do katalogu `outputs` z nazwą `oscar.txt`.

```bash
.
├── analyze_morphology.py
├── ...
└── outputs
    └── oscar.txt
```

## Uruchamianie

* Scrapowanie tweetów (tworzy katalog `scraped` z tweetami, można przerywać po każdym dniu i uruchamiać ponownie)

```bash
python scrape.py
```

* Utworzenie korpusu wzorcowego (tworzy plik `outputs/corpus.txt`)

```bash
python process_scraped.py
```

* Utworzenie korpusu pełnego (tworzy plik `outputs/nkjp.txt` i `outputs/full.txt`)

```bash
python process_nkjp.py
python assemble_full_corpus.py
```

* Utworzenie korpusu dla problemu (tworzy plik `outputs/problem.txt`)

```bash
python extract_problem.py
```

* Analiza morfologiczna (tworzy pliki `outputs/{full,corpus,problem}_analysis.csv`)

```bash
python analyze_morphology.py [-p num_processes]
```

* Analiza emoji

```bash
python emojis.py
```

* Generowanie chmur słów

```bash
./generate_wordclouds.sh
```

Pozostałe analizy znajdują się w poszczególnych notebookach.
