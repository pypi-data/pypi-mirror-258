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


def collapse_all(text: str) -> str:
    """
    Collapse all known full forms in the given text back into abbreviations.

    Args:
        text (str): The text containing full forms to collapse.

    Returns:
        str: The text with all full forms collapsed into abbreviations.
    """
    for abbreviation, full_form in abbreviations.items():
        text = re.sub(f'\\b{full_form}\\b', abbreviation, text, flags=re.IGNORECASE)
    return text


def collapse_one(text: str, full_form: str) -> str:
    """
    Collapse a specific full form in the given text back into its abbreviation.

    Args:
        text (str): The text containing the full form to collapse.
        full_form (str): The full form to collapse.

    Returns:
        str: The text with the specified full form collapsed into its abbreviation.

    Raises:
        KeyError: If the specified full form does not exist in the dictionary.
    """
    for abbreviation, ff in abbreviations.items():
        if ff.lower() == full_form.lower():
            text = re.sub(f'\\b{ff}\\b', abbreviation, text, flags=re.IGNORECASE)
            return text
    raise KeyError(f"Full form `{full_form}` does not exist in the abbreviations dictionary.")


def update_abbreviations(new_abbreviations: dict):
    """
    Update the abbreviations dictionary with more abbreviations.
    If an abbreviation key already exists, its value will be overwritten.

    Args:
        new_abbreviations (dict): A dictionary containing abbreviations and their full forms.
    """
    global abbreviations
    abbreviations.update(new_abbreviations)


def remove_abbreviations(abbreviations_to_remove: list):
    """
    Remove the specified abbreviations from the dictionary.

    Args:
        abbreviations_to_remove (list): A list of abbreviations to remove from the dictionary.
    """
    global abbreviations
    for abbreviation in abbreviations_to_remove:
        abbreviations.pop(abbreviation, None)
