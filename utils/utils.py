import hashlib
from collections import Counter
import re


def analyze_string(value: str) -> dict:
    """Compute string properties."""
    length = len(value)
    word_count = len(re.findall(r'\S+', value))
    is_palindrome = value.casefold() == value[::-1].casefold()
    unique_characters = len(set(value))
    sha256_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()
    frequency_map = dict(Counter(value))
    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency_map": frequency_map,
    }


def parse_natural_language(query: str):
    """
    Basic heuristic-based parser to interpret simple natural language queries.
    """
    q = query.lower().strip()
    filters = {}

    if "palindrom" in q:
        filters["is_palindrome"] = True
    if "single word" in q or "one word" in q:
        filters["word_count"] = 1
    if "longer than" in q:
        match = re.search(r"longer than (\d+)", q)
        if match:
            filters["min_length"] = int(match.group(1)) + 1
    if "containing the letter" in q:
        match = re.search(r"letter (\w)", q)
        if match:
            filters["contains_character"] = match.group(1)
    if "first vowel" in q:
        filters["contains_character"] = "a"

    if not filters:
        raise ValueError("Unable to parse natural language query")

    return filters
