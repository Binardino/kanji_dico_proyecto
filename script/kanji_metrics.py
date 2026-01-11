from pathlib import Path
from parse_unihan_cjkvi import (
    parse_unihan_cjkvi,
    normalise_unihan_dict,
    index_kangxi_radicals,
    build_variant_index,
    build_radical_dict,
    resolve_kanji_tree_enriched,
    load_kanji_resources
)


resources = load_kanji_resources(
    Path("../data/Unihan_CJKVI_database.txt"),
    Path("../data/kangxi_radicals.json")
)

KANJI_DB        = resources["KANJI_DB"]
RADICAL_DB      = resources["RADICAL_DB"]
KANGXI_RADICALS = resources["KANGXI_RADICALS"]
VARIANT_INDEX   = resources["VARIANT_INDEX"]

def tree_depth(node):
    """
   Compute the maximum depth of a kanji decomposition tree.

   The depth is defined as the number of levels from the current node
   down to the deepest leaf (inclusive).

   Parameters
   ----------
   node : dict
       A node of a kanji decomposition tree as returned by
       resolve_kanji_tree_enriched.

   Returns
   -------
   int
       The maximum depth of the tree.
   """
    # base case: a leaf node has a depth of 1
