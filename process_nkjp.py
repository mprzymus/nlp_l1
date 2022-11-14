import xml.etree.ElementTree as ET
from pathlib import Path

from tqdm import tqdm

from config import NKJP, NKJP_DIR


def extract_text(f: Path) -> None:
    root = ET.fromstring(f.read_text(encoding="utf-8"))

    with NKJP.open("a", encoding="utf-8") as output:
        for div in root.iter("{http://www.tei-c.org/ns/1.0}div"):
            for line in div:
                if not line.text:
                    continue

                output.write(line.text)
                output.write("\n")

            output.write("\n")


def main() -> None:
    files = list(NKJP_DIR.rglob("*text.xml"))
    for f in tqdm(files):
        extract_text(f)


if __name__ == "__main__":
    main()
