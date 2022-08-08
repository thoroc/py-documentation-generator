import pytest
from faker import Faker


@pytest.fixture(autouse=True)
def faker():
    return Faker()
