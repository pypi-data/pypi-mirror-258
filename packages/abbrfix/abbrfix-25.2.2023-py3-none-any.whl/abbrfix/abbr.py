import json
import re
from pathlib import Path

root = Path(__file__).parent

with open(root / 'abbreviations.json', 'r') as file:
    abbreviations = json.load(file)


def expand_all(text: str) -> str:
    """
    Expand all known abbreviations in the given text.

    Args:
        text (str): The text containing abbreviations to expand.

    Returns:
        str: The text with all abbreviations expanded.
    """
    for abbreviation, full_form in abbreviations.items():
        text = re.sub(f'\\b{abbreviation}\\b', full_form, text, flags=re.IGNORECASE)
    return text


def expand_one(text: str, abbreviation: str) -> str:
    """
    Expand a specific abbreviation in the given text.

    Args:
        text (str): The text containing the abbreviation to expand.
        abbreviation (str): The abbreviation to expand.

    Returns:
        str: The text with the specified abbreviation expanded.

    Raises:
        KeyError: If the specified abbreviation does not exist in the dictionary.
    """
    full_form = abbreviations.get(abbreviation)
    if not full_form:
        raise KeyError(f"Abbreviation `{abbreviation}` does not exist.")
    text = re.sub(f'\\b{abbreviation}\\b', full_form, text, flags=re.IGNORECASE)
    return text


def update_abbreviations(new_abbreviations: dict):
    """
    Update the abbreviations dictionary with more abbreviations.
    If an abbreviation key already exists, its value will be overwritten.

    Args:
        new_abbreviations (dict): A dictionary containing abbreviations and their full forms.
    """
    global abbreviations
    abbreviations.update(new_abbreviations)
