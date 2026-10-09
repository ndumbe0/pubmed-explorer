from app.utils.parsers import compute_hash, parse_authors, parse_keywords

def test_hash_consistency():
    h1 = compute_hash('Test Title', 2020, 'Test Journal', '10.1234/test')
    h2 = compute_hash('Different', 2021, 'Other', '10.1234/test')
    assert h1 == h2  # Same DOI gives same hash

def test_parse_authors():
    assert parse_authors('Alice; Bob') == ['Alice', 'Bob']
    assert parse_authors(['Alice', 'Bob']) == ['Alice', 'Bob']
    assert parse_authors('') == []
