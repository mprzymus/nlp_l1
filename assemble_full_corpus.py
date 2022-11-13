from pathlib import Path

NKJP_FILE = Path("nkjp.txt")
OSCAR_FILE = Path("oscar.txt")
OUTPUT_FILE = Path("full.txt")

MAX_SIZE = 1_073_741_824


def extract_to_full(f: Path) -> None:
    with (
        OUTPUT_FILE.open("a", encoding="utf-8") as output,
        f.open("r", encoding="utf-8") as input_,
    ):
        for line in input_:
            output.write(line.strip())
            output.write("\n")

            if OUTPUT_FILE.stat().st_size > MAX_SIZE and line == "\n":
                break


def main() -> None:
    extract_to_full(NKJP_FILE)
    extract_to_full(OSCAR_FILE)


if __name__ == "__main__":
    main()
