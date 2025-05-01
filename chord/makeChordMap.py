# 📄 File: chord/makeChordMap.py

from chord.chord_notes import CHORD_TO_NOTES
from pathlib import Path

def convert_to_symbol(chord_name: str) -> str:
    if chord_name.endswith("Major"):
        return chord_name[0]
    if chord_name.endswith("Minor"):
        return chord_name[0] + "m"
    if chord_name.endswith("maj7"):
        return chord_name[:-5] + "maj7"
    if chord_name.endswith("min9"):
        return chord_name[:-5] + "m9"
    if chord_name.endswith("dim"):
        return chord_name
    if chord_name.endswith("aug"):
        return chord_name[:-3] + "+"
    return chord_name

def generate_chord_symbol_map():
    return {name: convert_to_symbol(name) for name in CHORD_TO_NOTES}

def save_chord_symbol_map(output_file: Path):
    chord_map = generate_chord_symbol_map()
    code = "# Auto-generated chord symbol mapping\n\nCHORD_SYMBOL_MAP = " + repr(chord_map) + "\n"
    output_file.write_text(code, encoding="utf-8")
    print(f"✅ CHORD_SYMBOL_MAP.py 저장 완료 → {output_file}")

if __name__ == "__main__":
    output_path = Path(__file__).parent / "CHORD_SYMBOL_MAP.py"
    save_chord_symbol_map(output_path)