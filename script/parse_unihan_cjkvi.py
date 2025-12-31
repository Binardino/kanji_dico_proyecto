from pathlib import Path

def parse_unihan_cjkvi(path):
    IDS_OPERATORS = ("⿰", "⿱", "⿴", "⿵", "⿶","⿷", "⿸", "⿹", "⿺", "⿻")

    cjkvi_dict = {}

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            # skip empty lines or comments
            if not line or line.startswith("#"):
                continue
            
            #focus on Unihan codepoint lines
            if not line.startswith("U+"):
                continue

            parts = line.split('\t')

            #expected at least : codepoint, characfter, kanji decomposition entry
            if len(parts) < 3:
                continue

            #split each entry in 3 variables
            codepoint, char, ids = parts[:3]

            if not ids.startswith(IDS_OPERATORS):
                continue

            cjkvi_dict[char] = {
                                'codepoint': codepoint,
                                'ids'      : ids
                                }
    
    return cjkvi_dict

if __name__ == "__main__":
    path = Path("path/to/Unihan_CJKVI.txt")
    cjkvi_data = parse_unihan_cjkvi(path)
    for char, ids in cjkvi_data.items():
        print(f"Parsed {char}: {ids}")

            