from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA = DATA_DIR / "raw"
PROCESSED_DATA = DATA_DIR / "processed"

UNIHAN_CJKVI = RAW_DATA / "Unihan_CJKVI_database.txt"
KANJIDIC_XML = RAW_DATA / "kanjidic2.xml"
KANGXI_RADICALS_JSON = PROCESSED_DATA / "kangxi_radicals.json"
