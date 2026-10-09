from app.utils.parsers import compute_hash

def test_hash():
    h1 = compute_hash('Title', 2020, 'J', '10.1234/abc')
    h2 = compute_hash('Title', 2020, 'J', '10.1234/ABC')
    assert h1 == h2
