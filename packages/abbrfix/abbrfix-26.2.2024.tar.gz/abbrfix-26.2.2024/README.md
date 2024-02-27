# abbrfix

Library for expanding and collapsing abbreviations commonly used in online communication.

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

### Expand

```python
from abbrfix import expand_all, expand_one

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
```

### Collapse

```python
from abbrfix import collapse_all, collapse_one

# Example text with expanded abbreviations
text = "I'll be right back, got to go for lunch, talk to you later!"

# Collapse all abbreviations in the text
collapsed_text = collapse_all(text)
print(collapsed_text)
# Output: "I'll brb, gtg for lunch, ttyl!"

# Collapse a specific full form
collapsed_text = collapse_one(text, "talk to you later")
print(collapsed_text)
# Output: "I'll be right back, got to go for lunch, ttyl!"
```

### Update and Remove Abbreviations

```python
from abbrfix import update_abbreviations, remove_abbreviations

# Update the abbreviations dictionary with more abbreviations
new_abbreviations = {"lol": "laughing out loud", "omg": "oh my god"}
update_abbreviations(new_abbreviations)

# Remove abbreviations from the dictionary
abbreviations_to_remove = ["brb", "gtg"]
remove_abbreviations(abbreviations_to_remove)
```
