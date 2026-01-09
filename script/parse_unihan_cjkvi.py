from pathlib import Path
import re
import json

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
                                'codepoint'  : codepoint,
                                'raw_ids'    : raw_ids,
                                'ids'        : ids,
                                'parsed_ids' : parsed_ids,
                                'components' : components
                                }
    
    return cjkvi_dict
#%%
def normalise_kanji_entry(entry):
    """
    Normalise a kanji entry by removing annotations and extra spaces.
    """
    #case 1 - parsed with parse_ids_minimal
    if entry.get('parsed_ids') is not None:
        return {
            'codepoint'  : entry['codepoint'],
            'ids'        : entry['ids'],
            'components' : entry['components']
        }
    
    #case 2 - complex IDS - parse as tree
    try:
        tree       = parse_ids_trees(entry['ids'])
        components = extract_components_from_tree(tree)
        
        return {
            'codepoint'  : entry['codepoint'],
            'ids'        : entry['ids'],
            'components' : components
        }
    except Exception as e:
        print(f"Error parsing IDS tree for {entry['codepoint']}: {e}")
        pass

    
    #case 3 - unsupported IDS
    return {
    'codepoint'  : entry['codepoint'],
    'ids'        : entry['ids'],
    'components' : []
            }

def normalise_unihan_dict(unihan_dict):
    """
    Normalise the entire Unihan dictionary by processing each kanji entry.
    """
    normalised_dict = {}
    
    for char, entry in unihan_dict.items():
        normalised_dict[char] = normalise_kanji_entry(entry)
        
    return normalised_dict
#%%
def build_radical_dict(kanji_db, kangxi_radicals, variant_index):
    """
    Build a reverse dictionary : 
    radical -> all kanji using it
    """

    radical_dict = {}

    for kanji, data in kanji_db.items():
        for comp in data.get('components',  []):
            comp_char = comp['component']
            
            radical_char = variant_index.get(comp_char)

            if radical_char is None:
                continue

            if radical_char not in radical_dict:
                radical_dict[radical_char] = {
                    'radical_id' : kangxi_radicals[radical_char]['id'],
                    'name'       : kangxi_radicals[radical_char].get('name'),
                    'kanji'      : {}
                }

            radical_dict[radical_char]['kanji'][kanji] = {
                'position' : comp['position'],
                'ids_form' : comp_char
            }

    return radical_dict
def index_kangxi_radicals(kangxi_list):
    """
    Index Kangxi radicals by their canonical radical form.
    Key = radical character used in IDS (e.g. 一, 丨, 丶)
    """
    indexed = {}

    for r in kangxi_list:
        radical_char = r["radical"]

        indexed[radical_char] = {
            "id": r["number"],
            "kangxi_radical": r["kangxi_radical"],
            "code": r["code"],
            "english_name": r["english_name"],
            "meaning": r["meaning"],
            "strokes": r["strokes"],
            "variants": r.get("variants", []),
            "notes": r.get("notes", "")
        }

    return indexed

def build_variant_index(kangxi_radicals):
    """
    Build a mapping dict from IDS variant forms to canonical Kangxi radicals.
    e.g. 
    VARIANT_TO_RADICAL = {
    "氵": "水",
    "忄": "心",
    "扌": "手",
    "礻": "示",
    "衤": "衣",
    "⻌": "辵"
    }
    """
    variant_index = {}
    
    for radical, data in kangxi_radicals.items():
        variant_index[radical] = radical
        
        for variant in data.get('variants', []):
            variant_index[variant] = radical
            
    return variant_index
#%%
def resolve_kanji_tree(char, kanji_db, visited=None):
    """
    Core function.
    Recursively resolve a kanji into its full component tree of atomic components.
    Gives core recursive structure for kanji decomposition.
    Structural gold standard.
    """

    if visited is None:
        visited = set()

    #avoid infinite loops
    if char in visited:
        return {'char': char, 'children': []}
    
    visited.add(char)

    entry = kani_db.get(char)

    #character not found in database or already atomic
    if entry is None or not entry['components']:
        return {'char': char, 'children': []}
    
    children = []
    for component in entry['components']:
        child_char = component['component']
        subtree = resolve_kanji_tree(child_char, kanji_db, visited)
        children.append()

        return {
            'char': char,
            'children': children
        }

def resolve_kanji_tree_enriched(char, kanji_db, variant_index, kangxi_radicals, visited=None, position=None):
    """Enriched version of resolve_kanji_tree with additional metadata.
       Enriched view of the kanji decomposition tree.
    1. is_leaf: whether the node is an atomic component (no further decomposition)
    2. is_radical: whether the node is a Kangxi radical (canonical or variant)
    3. position: the position of the component within its parent kanji (if applicable)
    """

    if visited is None:
        visited = set()

    if char in visited:
        return {'char'      : char, 
                'position'  : position,
                'is_leaf'   : True,
                'is_radical': False,
                'children'  : []
                }
    
    visited.add(char)

    entry      = kanji_db.get(char)
    components = entry['components'] if entry else []

    is_leaf = not components

    #is it a radical? canonical or variant
    canonical_radical = variant_index.get(char)
    is_radical = canonical_radical in kangxi_radicals if canonical_radical else False

    node = {
        'char'       : char,
        'position'   : position,
        'is_leaf'    : is_leaf,
        'is_radical' : is_radical,
        'children'   : []
    }

    for component in components:
        child_char = component['component']
        child_position = component['position']

        subtree = resolve_kanji_tree_enriched(
            child_char, 
            kanji_db, 
            variant_index, 
            kangxi_radicals, 
            visited, 
            position=child_position
        )
        node['children'].append(subtree)

    return node
        #%%
tree = resolve_kanji_tree("海", KANJI_DB)
from pprint import pprint
pprint(tree)
#%%
if __name__ == "__main__":
    path = Path("../data/Unihan_CJKVI_database.txt")
    raw_cjkvi_data = parse_unihan_cjkvi(path)
    for char, ids in raw_cjkvi_data.items():
        print(f"Parsed {char}: {ids}")

    KANJI_DB = normalise_unihan_dict(raw_cjkvi_data)
    with open('../data/kangxi_radicals.json', 'r', encoding='utf-8') as f:
        KANGXI_RADICALS_LIST = json.load(f)

    KANGXI_RADICALS = index_kangxi_radicals(KANGXI_RADICALS_LIST)
    VARIANT_INDEX = build_variant_index(KANGXI_RADICALS)
    RADICAL_DB = build_radical_dict(KANJI_DB, KANGXI_RADICALS, VARIANT_INDEX)
#%%

parsed = parse_ids_minimal("⿰氵毎")
ids_to_positioned_components(parsed)
#%% TEST
unihan_data = parse_unihan_cjkvi(path)
parsed = parse_ids_minimal(unihan_data["海"]["ids"])

# 3. Interprétation en positions
components = ids_to_positioned_components(parsed)
#%%
ids = unihan_data["海"]["ids"]
parsed = parse_ids_minimal(ids)

if parsed is None:
    print("IDS non supporté :", repr(ids), "len =", len(ids))
    
ids = unihan_data["海"]["ids"]
print(ids, len(ids), [c for c in ids])

            