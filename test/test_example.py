import pytest

def test_equal_or_not():
    assert 1 == 1

def test_is_isInstance():
    assert isinstance('test', str)
    assert not isinstance('10', int)
