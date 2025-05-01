from pathlib import Path
import re

def read_text_file(filepath: Path) -> str:
    """Reads the content of the input file."""
    return filepath.read_text(encoding='utf-8')

def split_into_sentences(text: str) -> list:
    """
    Splits text into sentences while preserving all original punctuation.
    """
    # Matches sentence-ending punctuation (., ?, !) followed by space or end of line
    pattern = re.compile(r'(.*?[.!?।]["\']?(?:\s+|$))', re.DOTALL)
    return [match.group(1) for match in pattern.finditer(text)]

def write_each_sentence_to_file(sentences: list, output_dir: Path):
    """Writes each sentence into a separate file."""
    output_dir.mkdir(exist_ok=True)
    for idx, sentence in enumerate(sentences):
        filename = f"{str(idx + 1).zfill(5)}.txt"
        (output_dir / filename).write_text(sentence, encoding='utf-8')

def main():
    input_file = Path(r"story\Flames CH 01.txt")
    output_dir = Path("story_fragments") / input_file.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    text = read_text_file(input_file)
    sentences = split_into_sentences(text)
    write_each_sentence_to_file(sentences, output_dir)

    print(f"{len(sentences)} sentence files saved to: {output_dir.resolve()}")

if __name__ == "__main__":
    main()
