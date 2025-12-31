from pathlib import Path

def parse_unihan_cjkvi(path):
    IDS_OPERATORS = ("⿰", "⿱", "⿴", "⿵", "⿶","⿷", "⿸", "⿹", "⿺", "⿻")

    cjkvi_dict = {}

    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            #skip empty lines
            if not line or line.startswith('#'):
                continue

            parts = line.split('\t')

            #expected at least : codepoint, characfter, kanji decomposition entry
            if len(parts) < 3:
                continue

            _, char, ids = parts[:3]

            cjkvi_dict[char] = ids
    
    return cjkvi_dict

if __name__ == "__main__":
    path = Path("path/to/Unihan_CJKVI.txt")
    cjkvi_data = perse_unihan_cjkvi(path)
    for char, ids in cjkvi_data.items():
        print(f"Parsed {char}: {ids}")

            