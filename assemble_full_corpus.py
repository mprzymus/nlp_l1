from pathlib import Path

from config import FULL, NKJP, OSCAR

MAX_SIZE = 1_073_741_824


def extract_to_full(f: Path) -> None:
    with (
        FULL.open("a", encoding="utf-8") as output,
        f.open("r", encoding="utf-8") as input_,
    ):
        for line in input_:
            output.write(line.strip())
            output.write("\n")

            if FULL.stat().st_size > MAX_SIZE and line == "\n":
                break


def main() -> None:
    extract_to_full(NKJP)
    extract_to_full(OSCAR)


if __name__ == "__main__":
    main()
