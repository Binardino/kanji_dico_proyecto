from pathlib import Path
import re

#%%
def clean_ids(ids):
    """
    Remove Unihan annotations like [GTKV] from IDS strings to keep IDS clean.
    """
    IDS_ANNONATION_REGEX = re.compile(r"\[.*?\]$")
    
    return IDS_ANNONATION_REGEX.sub("", ids)
#%%
def ids_to_positioned_components(parsed_ids):
    operator = parsed_ids['operator']
    children = parsed_ids['children']
    
    left_pos, right_pos = IDS_BINARY_OPERATORS[operator]
    
    return [
            {'component': children[0], 'position' : left_pos},
            {'component': children[1], 'position' : right_pos}
            ]
#%%
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

            