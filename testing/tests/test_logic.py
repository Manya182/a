import pytest
from app.logic import iseligible


def test_eligible():
    assert iseligible(12)==True