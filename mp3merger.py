from pathlib import Path
from pydub import AudioSegment

output_dir = Path(r"D:\paradise\Audiobook\hindi")  # Change this to your desired output directory

def get_mp3_files(folder: Path) -> list[Path]:
    """Return a sorted list of .mp3 files in the given folder."""
    return sorted(folder.glob("*.mp3"))

def merge_mp3_files(mp3_files: list[Path]) -> AudioSegment:
    """Merge a list of mp3 files into a single AudioSegment."""
    merged = AudioSegment.empty()
    for file in mp3_files:
        print(f"Adding: {file.name}")
        merged += AudioSegment.from_mp3(file)
    return merged

def save_merged_audio(audio: AudioSegment, output_path: Path) -> None:
    """Export the merged audio to the given path."""
    audio.export(output_path, format="mp3")
    print(f"Merged audio saved to: {output_path}")

def process_single_folder(folder: Path) -> None:
    """Process a single folder containing mp3 files."""
    mp3_files = get_mp3_files(folder)
    if not mp3_files:
        print(f"No mp3 files found in {folder}")
        return
    merged_audio = merge_mp3_files(mp3_files)
    output_file = output_dir / folder.name
    output_file.mkdir(parents=True, exist_ok=True)
    output_file = output_file / f"{folder.name}.mp3"
    save_merged_audio(merged_audio, output_file)

def batch_process(root_folder: Path) -> None:
    """Process all subfolders under root_folder that contain mp3 files."""
    print(f"Starting batch processing in: {root_folder}")
    for subfolder in root_folder.iterdir():
        if subfolder.is_dir():
            print(f"\nProcessing folder: {subfolder}")
            process_single_folder(subfolder)

if __name__ == "__main__":
    # Update this path to the parent folder containing MP3 subfolders
    root = Path("downloads")  # <-- Change as needed
    batch_process(root)
