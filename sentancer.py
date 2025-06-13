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
    pattern = re.compile(r'(.*?[.!?।।]["\']?(?:\s+|$))', re.DOTALL)
    return [match.group(1) for match in pattern.finditer(text) if match.group(1).strip()]

def write_grouped_sentences_to_file(sentences: list, output_dir: Path, max_chars: int = 500):
    """Writes sentences into files, each file not exceeding max_chars, and no sentence is split."""
    output_dir.mkdir(exist_ok=True)
    file_idx = 1
    buffer = ""

    for sentence in sentences:
        sentence = sentence.strip()
        # If a single sentence is longer than max_chars, write it alone
        if len(sentence) > max_chars:
            breakpoint()
            if buffer:
                filename = f"{str(file_idx).zfill(5)}.txt"
                (output_dir / filename).write_text(buffer.strip(), encoding='utf-8')
                file_idx += 1
                buffer = ""
            sub_sentences = re.split(r'[-;,।।]|(?:\b(?:और|lekin)\b)', sentence)
            for sub_sentence in sub_sentences:
                sub_sentence = sub_sentence.strip()
                if sub_sentence:
                    filename = f"{str(file_idx).zfill(5)}.txt"
                    (output_dir / filename).write_text(sub_sentence, encoding='utf-8')
                    file_idx += 1
        elif len(buffer) + len(sentence) <= max_chars:
            buffer += sentence + " "
        else:
            filename = f"{str(file_idx).zfill(5)}.txt"
            (output_dir / filename).write_text(buffer.strip(), encoding='utf-8')
            file_idx += 1
            buffer = sentence + " "

    # Write remaining buffer
    if buffer.strip():
        filename = f"{str(file_idx).zfill(5)}.txt"
        (output_dir / filename).write_text(buffer.strip(), encoding='utf-8')

def main():
    input_dir = Path("story")
    for input_file in input_dir.glob("*.txt"):

        # input_file = Path(r"story\Flames CH 01.txt")
        output_dir = Path("story_fragments") / input_file.stem
        output_dir.mkdir(parents=True, exist_ok=True)

        text = read_text_file(input_file)
        sentences = split_into_sentences(text)
        write_grouped_sentences_to_file(sentences, output_dir)

        print(f"Sentence groups saved to: {output_dir.resolve()}")

if __name__ == "__main__":
    main()
