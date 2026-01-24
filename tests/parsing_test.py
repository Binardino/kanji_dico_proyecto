
#%% test

parsed = parse_ids_minimal("⿰氵毎")
ids_to_positioned_components(parsed)

#%%
tree = resolve_kanji_tree("海", KANJI_DB)
from pprint import pprint
pprint(tree)
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

            
