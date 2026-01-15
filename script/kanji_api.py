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
