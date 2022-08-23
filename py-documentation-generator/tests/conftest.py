from collections import namedtuple
from pathlib import Path
from git import Repo
import pytest
from loguru import logger


Author = namedtuple("Author", "name email committer")


@pytest.fixture(autouse=True)
def remove_url(faker):
    return f"https://{faker.hostname()}/{faker.word()}/{faker.word()}"


@pytest.fixture(autouse=True)
def name(faker):
    return faker.name()


@pytest.fixture(autouse=True)
def email(faker, name):
    joining_char = faker.random_element(elements=[".", "-", "_", ""])
    email_local_part = f"{joining_char.join(name.lower().split(' '))}"
    return f"{email_local_part}@{faker.free_email_domain()}"


@pytest.fixture(autouse=True)
def author(name, email):
    return Author(
        name=name,
        email=email,
        committer=f"{name} <{email}>"
    )


@pytest.fixture(autouse=True)
def local_repo(tmp_path_factory, faker):
    tmp_dir = tmp_path_factory.mktemp("data")

    repo = Repo.init(tmp_dir, initial_branch=f"{faker.word()}")

    file = Path(tmp_dir) / "README.md"
    file.write_text("# README")

    repo.git.add(file)
    repo.git.commit("-m", "initial commit",
                    author=f"test-bot <test-bot@{faker.free_email_domain()}>")

    logger.debug("Initialised Repo on: {}", tmp_dir)

    yield repo
