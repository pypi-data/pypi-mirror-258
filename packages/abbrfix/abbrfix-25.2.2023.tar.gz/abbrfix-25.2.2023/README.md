# abbrfix

abbrfix is a Python library for expanding abbreviations commonly used in online communication.

## Installation

To install the library, use pip:

```bash
pip install abbrfix
```

Alternatively, install the latest directly from the GitHub repository:

```bash
pip install git+https://github.com/dsymbol/abbrfix.git
```

## Usage

```python
from abbrfix import expand_all, expand_one, update_abbreviations

# Example text with abbreviations
text = "I'll brb, gtg for lunch, ttyl!"

# Expand all abbreviations in the text
expanded_text = expand_all(text)
print(expanded_text)
# Output: "I'll be right back, got to go for lunch, talk to you later!"

# Expand a specific abbreviation
expanded_text = expand_one(text, "brb")
print(expanded_text)
# Output: "I'll be right back, gtg for lunch, ttyl!"

# Update the abbreviations dictionary with more abbreviations
new_abbreviations = {"lol": "laughing out loud", "omg": "oh my god"}
update_abbreviations(new_abbreviations)
```
