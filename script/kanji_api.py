import logging
from pathlib import Path

#import core loading & computation utilities
from parse_unihan_cjkvi import load_kanji_resources
from kanji_metrics import kanji_complexity_metrics

#import tree resolution - internal use
from parse_unihan_cjkvi import resolve_kanji_tree_enriched

#logger setup
logger = logging.getLogger('kanji_api')

#load resources
RESOURCES = load_kanji_resources(
                Path("../data/Unihan_CJKVI_database.txt"),
                Path("../data/kangxi_radicals.json")
            )

KANJI_DB        = RESOURCES["KANJI_DB"]
RADICAL_DB      = RESOURCES["RADICAL_DB"]
KANGXI_RADICALS = RESOURCES["KANGXI_RADICALS"]
VARIANT_INDEX   = RESOURCES["VARIANT_INDEX"]

#%%
#Public API functions

def kanji_exists(kanji):
    """
    Check whether a kanji exists in the DB
    """

    return kanji in KANJI_DB

def radical_exists(radical):
    """
    Check whether a radical (or its variant) exists in the database.
    """
    return radical in RADICAL_DB or radical in VARIANT_INDEX
