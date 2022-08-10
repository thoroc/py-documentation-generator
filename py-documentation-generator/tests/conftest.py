from collections import namedtuple
import pytest
from faker import Faker

Personalia = namedtuple("Personalia", "name email")


@pytest.fixture(autouse=True)
def faker():
    return Faker()


@pytest.fixture(autouse=True)
def fake_repo(faker):
    return f"https://{faker.hostname()}/{faker.word()}/{faker.word()}"


@pytest.fixture(autouse=True)
def fake_personalia(faker):
    name = faker.name()
    joining_char = faker.random_element(elements=[".", "-", "_", ""])
    email_local_part = f"{joining_char.join(name.lower().split(' '))}"
    # return {
    #     "name": faker.name(),
    #     "email": f"{email_local_part}@{faker.free_email_domain()}",
    # }
    return Personalia(
        name=faker.name(),
        email=f"{email_local_part}@{faker.free_email_domain()}",
    )
