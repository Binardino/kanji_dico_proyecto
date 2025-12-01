import json
import re

#check if each dict enty has all required fields
REQUIRED_FIELDS = ["number",
                    "kangxi_radical",
                    "radical",
                    "code",
                    "english_name",
                    "meaning",
                    "strokes",
                    "variants",
                    "notes"
                    ]

CODE_PATTERN = re.compile(r"U\+2F[0-9A-F}{2}")

def load_radicals(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def check_required_keys(kangxi_radical, errors):
    for field in REQUIRED_FIELDS:
        if field not in kangxi_radical:
            errors.append(f"Missing field '{field}' in kangxi_radical #{kangxi_radical.get('number')}")
        
        else:
            if field == "variants" and not isinstance(kangxi_radical[field], list):
                errors.append(f"'variants' must be a list in kangxi_radical #{kangxi_radical['number']}")
                
def check_numbering(radicals, errors):
    numbers = [rad['number'] for rad in radicals]
    
    if sorted(numbers) != list(range(1,215)):
        errors.append('Numbering error : radicals should be numbered between 1 & 214 exactly')
        
    if len(numbers) != len(set(numbers)):
        errors.append('Numbering error : duplicate radical number detected')