import re
import hashlib
import unicodedata

def slugify(value: str) -> str:
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = str(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def generate_short_hash(value: str, length: int = 5) -> str:
    """
    Generates a short hash from a string.
    """
    hash_object = hashlib.md5(value.encode())
    return hash_object.hexdigest()[:length]

def generate_filename(name: str, identifier: str) -> str:
    """
    Generates a filename with the format: slugified_name + hash(5 chars).format
    """
    slug = slugify(name)
    short_hash = generate_short_hash(identifier)
    return f"{slug}-{short_hash}"
