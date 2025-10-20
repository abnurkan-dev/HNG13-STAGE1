from typing import Dict, List, Optional
from datetime import datetime
from models.models import StringItem, StringProperties
from utils.utils import analyze_string

# In-memory storage (acting as DB)
string_store: Dict[str, StringItem] = {}


def create_string(value: str) -> StringItem:
    props = analyze_string(value)
    if props["sha256_hash"] in string_store:
        raise ValueError("exists")

    item = StringItem(
        id=props["sha256_hash"],
        value=value,
        properties=StringProperties(**props),
        created_at=datetime.utcnow(),
    )
    string_store[item.id] = item
    return item


def get_string(value: str) -> Optional[StringItem]:
    from hashlib import sha256
    hash_val = sha256(value.encode("utf-8")).hexdigest()
    return string_store.get(hash_val)


def delete_string(value: str) -> bool:
    from hashlib import sha256
    hash_val = sha256(value.encode("utf-8")).hexdigest()
    if hash_val not in string_store:
        return False
    del string_store[hash_val]
    return True


def list_strings(
    is_palindrome: Optional[bool] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    word_count: Optional[int] = None,
    contains_character: Optional[str] = None,
) -> List[StringItem]:
    results = list(string_store.values())

    def matches(item: StringItem):
        p = item.properties
        if is_palindrome is not None and p.is_palindrome != is_palindrome:
            return False
        if min_length is not None and p.length < min_length:
            return False
        if max_length is not None and p.length > max_length:
            return False
        if word_count is not None and p.word_count != word_count:
            return False
        if contains_character and contains_character not in item.value:
            return False
        return True

    return [x for x in results if matches(x)]
