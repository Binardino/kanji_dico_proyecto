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

CODE_PATTERN = re.compile(r"U\+2F[0-9A-F]{2}")

def load_radicals(path):
    """
    Load the Kangxi radicals dataset from a JSON file.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the JSON file containing the radicals dataset.
    
    Returns
    -------
    list[dict] - list of radical dictionaries loaded from the file.
    """

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def check_required_keys(kangxi_radical, errors):
    """
    Validate that a radical entry contains all required fields.
    
    Parameters
    ----------
    kangxi_radical : dict
        A dictionary representing a single Kangxi radical entry.
    errors : list[str]
        A list to which error messages will be appended.
    
    Side Effects
    ------------
    Appends descriptive validation error messages to `errors` if:
        - a required field is missing
        - the 'variants' field exists but is not a list
    
    Notes
    -----
    This function does not validate the *contents* of each field, only their
    presence and basic type correctness.
    """
    
    for field in REQUIRED_FIELDS:
        if field not in kangxi_radical:
            errors.append(f"Missing field '{field}' in kangxi_radical #{kangxi_radical.get('number')}")
        
        else:
            if field == "variants" and not isinstance(kangxi_radical[field], list):
                errors.append(f"'variants' must be a list in kangxi_radical #{kangxi_radical['number']}")
                
def check_numbering(radicals, errors):
    """
    Verify that radical numbering is correct, continuous, and contains no duplicates.

    Parameters
    ----------
    radicals : list[dict]
        List of radical entries. Each entry must contain a `number` field.
    errors : list[str]
        A list to which error messages will be appended.

    Side Effects
    ------------
    Appends error messages to `errors` if:
        - numbers are not exactly 1 through 214
        - radical numbers are duplicated

    Notes
    -----
    This check ensures the structural integrity of the dataset's numbering
    system but does not validate the content of each radical.
    """
    numbers = [rad['number'] for rad in radicals]
    
    if sorted(numbers) != list(range(1,215)):
        errors.append('Numbering error : radicals should be numbered between 1 & 214 exactly')
        
    if len(numbers) != len(set(numbers)):
        errors.append('Numbering error : duplicate radical number detected')

def check_unicode_code(radical, errors):
    """
    Validate that the radical's Unicode code field is well-formed and consistent.

    Parameters
    ----------
    radical : dict
        A dictionary representing a single Kangxi radical entry. 
        Must contain a 'code' and 'number' field.
    errors : list[str]
        A list to which error messages will be appended.

    Side Effects
    ------------
    Appends an error to `errors` if the `code` field does not match 
    the expected format defined by CODE_PATTERN (e.g., 'U+2F00').

    Notes
    -----
    This validation does not check the semantic correctness of the codepoint
    (e.g., whether it matches the radical glyph); it only checks the string
    format. Additional semantic validation is handled elsewhere.
    """
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
    Verify that the radical's Unicode codepoint matches its Kangxi radical number.

    Parameters
    ----------
    radical : dict
        A dictionary representing a single Kangxi radical entry. Must contain
        'number' and 'code' fields.
    errors : list[str]
        A list to which error messages will be appended.

    Side Effects
    ------------
    Appends an error message to `errors` if the Unicode codepoint derived from
    the radical number does not match the declared `code` field.

    Notes
    -----
    According to the Unicode standard, Kangxi radicals occupy the contiguous
    block U+2F00–U+2FD5. The expected relationship is:

        codepoint == 0x2F00 + (number - 1)

    This function enforces that invariant to detect off-by-one shifts and
    ordering errors.
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


def validate_radicals(radicals):
    """
    Validate the variants field of a Kangxi radical entry.

    Parameters
    ----------
    radical : dict
        A dictionary representing a single Kangxi radical entry. Must contain
        a 'variants' field.
    errors : list[str]
        A list to which error messages will be appended.

    Side Effects
    ------------
    Appends error messages to `errors` if:
        - a variant contains leading or trailing whitespace
        - a variant is not a single Unicode character
        - duplicate variants are detected

    Notes
    -----
    Kangxi radical variants are expected to be individual Unicode glyphs.
    This function does not modify the dataset; it only reports inconsistencies.
    """
    errors = []

    # global structure checks
    check_numbering(radicals, errors)

    # individual radical checks
    for radical in radicals:
        check_required_keys(radical, errors)
        check_unicode_code(radical, errors)
        check_sequential_unicode(radical, errors)
        check_variants(radical, errors)

        # strokes sanity
        if not isinstance(radical["strokes"], int) or radical["strokes"] <= 0:
            errors.append(f"Invalid stroke count in radical #{radical['number']}")

        # english_name & meaning should not be empty
        if not radical["english_name"]:
            errors.append(f"Empty english_name for radical #{radical['number']}")
        if not radical["meaning"]:
            errors.append(f"Empty meaning for radical #{radical['number']}")

    return errors

def main():
    radicals = load_radicals("../data/kangxi_radicals.json")
    errors   = validate_radicals(radicals)

    if not errors:
        print("✓ All radicals passed validation with no errors.")
    else:
        print("❌ Validation errors detected:")
        for e in errors:
            print(" -", e)
    return errors

if __name__ == "__main__":
    errors = main()
