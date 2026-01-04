from pathlib import Path
import re

IDS_OPERATORS        = ("⿰", "⿱", "⿴", "⿵", "⿶","⿷", "⿸", "⿹", "⿺", "⿻")

IDS_BINARY_OPERATORS = {
                        "⿰": ("left", "right"),
                        "⿱": ("top", "bottom"),
                    }

#%%
def clean_ids(ids):
    """
    Remove Unihan annotations like [GTKV] from IDS strings to keep IDS clean.
    """
    IDS_ANNONATION_REGEX = re.compile(r"\[.*?\]$")
    
    return IDS_ANNONATION_REGEX.sub("", ids)
#%%
def parse_ids_minimal(ids):
    if not ids:
        return
    
    operator = ids[0]
    
    #only handle simple binary operators for now
    if operator not in IDS_BINARY_OPERATORS:
        return None
    
    #minimal binary IDs must be exactly 3 characters long
    if len(ids) != 3:
        return None
    
    left  = ids[1]
    right = ids[2]
    
    return {"operator" : operator,
            "children" : [left, right]
        }

parse_ids_minimal("⿰氵毎")
parse_ids_minimal("⿱⺊一")
parse_ids_minimal("⿱一⿰丿𠃌")
#%%
def parse_ids_trees(ids):
    """
    Parse IDS strings into tree structures.
    """
    def _parse(index):
        child = ids[index]

        if child in IDS_OPERATORS:
            operator = child
            left_child, next_index  = _parse(index + 1)
            right_child, next_index = _parse(next_index)

            return {
                'operator': operator, 
                'children': [left_child, right_child]}, next_index

        return {'char': child}, index + 1

    tree, final_index = _parse(0)

    if final_index != len(ids):
        raise ValueError("IDS string could not be fully parsed.")

    return tree    

parse_ids_trees('⿰⿱亠口心')
#%%
def ids_to_positioned_components(parsed_ids):
    operator = parsed_ids['operator']
    children = parsed_ids['children']
    
    if operator not in IDS_BINARY_OPERATORS:
        raise ValueError(f"Unsupported operator in minimal IDS: {operator}")
    
    left_pos, right_pos = IDS_BINARY_OPERATORS[operator]
    
    return [
            {'component': children[0], 'position' : left_pos},
            {'component': children[1], 'position' : right_pos}
            ]
#%% 
def extract_components_from_tree(tree, position=None):
    """
    Flatten an IDS tree into positioned atomic components.
    """
    if 'char' in tree:
        return [{
            'component' : tree['char'], 
            'position'  : position
            }]
    operator = tree['operator']
    left_pos, right_pos = IDS_BINARY_OPERATORS.get(operator, (None, None))

    left, right = tree['children']

    components = []
    components.extend(extract_components_from_tree(left, left_pos))
    components.extend(extract_components_from_tree(right, right_pos))

    return components
#%%
def parse_unihan_cjkvi(path):
    """
    Parse the Unihan_CJKVI file and extract IDS decompositions.

    Parameters
    ----------
    path : str or Path
        Path to the Unihan_CJKVI text file.

    Returns
    -------
    dict[str, dict]
        Dictionary mapping a character to its Unicode codepoint and IDS string.
        Example:
        {
          "上": {"codepoint": "U+4E0A", "ids": "⿱⺊一"}
        }
    """
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
            codepoint, char, raw_ids = parts[:3]
            
            #clean IDS
            ids = clean_ids(raw_ids)
            
            #parse IDS minimal
            parsed_ids = parse_ids_minimal(ids)
            
            #derive positioned components
            if parsed_ids is not None:
                components = ids_to_positioned_components(parsed_ids)
            else:
                components = None

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

            