from src.core.utils import slugify, generate_short_hash, generate_filename

def test_slugify():
    assert slugify("Hello World!") == "hello-world"
    assert slugify("  Spaced   String  ") == "spaced-string"
    assert slugify("Café & Restaurant") == "cafe-restaurant"
    assert slugify("User-Name_123") == "user-name_123"

def test_generate_short_hash():
    hash1 = generate_short_hash("test")
    hash2 = generate_short_hash("test")
    hash3 = generate_short_hash("other")
    
    assert len(hash1) == 5
    assert hash1 == hash2
    assert hash1 != hash3

def test_generate_filename():
    filename = generate_filename("My Video", "unique-id")
    assert filename.startswith("my-video-")
    assert len(filename.split("-")[-1]) == 5
