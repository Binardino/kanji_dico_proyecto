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

def check_unicode_code(radical, errors):
    code = radical["code"]
    if not CODE_PATTERN.fullmatch(code):
        errors.append(f"Invalid code format '{code}' in radical #{radical['number']}")

    # check kangxi_radical matches code
    expected_char = chr(int(code[2:], 16))
    if radical["kangxi_radical"] != expected_char:
        errors.append(
            f"Unicode mismatch in radical #{radical['number']}: "
            f"code {code} produces '{expected_char}' "
            f"but kangxi_radical is '{radical['kangxi_radical']}'"
        )

def check_sequential_unicode(radical, errors):
    """
    Check that radical number n matches Unicode U+2F00 + (n-1)
    This holds for all 214 radicals in the official Kangxi block.
    """
    n = radical["number"]
    expected_codepoint = 0x2F00 + (n - 1)
    actual_codepoint = int(radical["code"][2:], 16)

    if expected_codepoint != actual_codepoint:
        errors.append(
            f"Sequential Unicode mismatch at #{n}: "
            f"expected U+{expected_codepoint:04X}, got {radical['code']}"
        )

def check_variants(radical, errors):
    variants = radical["variants"]

    # check duplicates
    if len(variants) != len(set(variants)):
        errors.append(f"Duplicate variants in radical #{radical['number']}")

    # check all variants are single glyphs
    for v in variants:
        if len(v) != 1:
            errors.append(
                f"Variant '{v}' in radical #{radical['number']} "
                f"is not a single character."
            )