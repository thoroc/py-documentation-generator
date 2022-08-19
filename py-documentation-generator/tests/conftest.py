from collections import namedtuple
from git import Repo
import pytest

Personalia = namedtuple("Personalia", "name email")


@pytest.fixture(autouse=True)
def fake_remote_repo(faker):
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


@pytest.fixture(autouse=True)
def fake_local_repo(tmp_path_factory, faker):
    path = tmp_path_factory.mktemp("data")

    repo = Repo.init(path)

    return repo
