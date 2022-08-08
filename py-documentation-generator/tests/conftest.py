import pytest
from faker import Faker


@pytest.fixture(autouse=True)
def faker():
    return Faker()


@pytest.fixture(autouse=True)
def fake_repo(faker):
    return f"https://{faker.hostname()}/{faker.word()}/{faker.word()}"
