from collections import namedtuple
from pathlib import Path
from git import Repo
import pytest
from loguru import logger
from src.models.contributor import Contributor


@pytest.fixture(autouse=True)
def remove_url(faker):
    faker.random.seed()
    return f"https://{faker.hostname()}/{faker.word()}/{faker.word()}"


@pytest.fixture(autouse=True)
def name(faker):
    faker.random.seed()
    return faker.name()


@pytest.fixture(autouse=True)
def email(faker, name):
    faker.random.seed()
    joining_char = faker.random_element(elements=[".", "-", "_", ""])
    email_local_part = f"{joining_char.join(name.lower().split(' '))}"
    return f"{email_local_part}@{faker.free_email_domain()}"


@pytest.fixture(autouse=True)
def contributor(name, email):
    return Contributor(
        name=name,
        email=email,
        commits=[]
    )


@pytest.fixture(autouse=True, scope="function")
def local_repo(tmp_path_factory, faker):
    faker.random.seed()
    tmp_dir = tmp_path_factory.mktemp("data")

    repo = Repo.init(tmp_dir, initial_branch=f"{faker.word()}")

    file = Path(tmp_dir) / "README.md"
    file.write_text("# README")

    repo.git.add(file)
    repo.git.commit("-m", "initial commit",
                    author=f"test-bot <test-bot@{faker.free_email_domain()}>")

    logger.debug("Initialised Repo on: {}", tmp_dir)

    yield repo

    repo.git.rm(tmp_dir, r=True)
