from pathlib import Path
import re

def read_text_file(filepath: Path) -> str:
    """Reads the content of a text file."""
    return filepath.read_text(encoding='utf-8')

def split_into_sentences(text: str) -> list:
    """Splits text into sentences using punctuation like . ! ?"""
    return re.split(r'(?<=[.!?।])\s+', text)

def write_each_sentence_to_file(sentences: list, output_dir: Path):
    """Writes each sentence to a separate file with zero-padded filenames."""
    output_dir.mkdir(exist_ok=True)
    
    for idx, sentence in enumerate(sentences):
        filename = f"{str(idx + 1).zfill(5)}.txt"
        file_path = output_dir / filename
        file_path.write_text(sentence, encoding='utf-8')

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
