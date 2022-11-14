from datasets import load_dataset
from pyarrow.lib import StringScalar

from config import CONTENT_LINK_REGEX, PROBLEM


def extract(lines: list[StringScalar]) -> None:
    with PROBLEM.open("a", encoding="utf-8") as f:
        for line in lines:
            line = (
                line.as_py()
                .replace("\\n", "\n")
                .replace(r"\"", '"')
                .replace("\n\n", "\n")
                .replace("\\u0026amp;", "&")
                .replace("\\u0026gt;", ">")
                .replace("\\u0026lt;", "<")
                .replace("\\\\", "\\")
            )
            line = CONTENT_LINK_REGEX.sub("", line)

            f.write(line.strip())
            f.write("\n\n")


def main() -> None:
    dataset = load_dataset("poleval2019_cyberbullying", "task01")

    for subset in dataset:
        extract(dataset.data[subset]["text"])  # type: ignore


if __name__ == "__main__":
    main()
