from pathlib import Path
from git import Repo, Commit
import pytest
from loguru import logger
from src.models.contributor import Contributor


@pytest.fixture(autouse=True)
def remote_url(faker):
    faker.random.seed()
    return f"https://{faker.hostname()}/{faker.word()}/{faker.word()}"


@pytest.fixture(autouse=True)
def name(faker):
    faker.random.seed()
    return faker.name()


@pytest.fixture(autouse=True)
def email(faker, name: str):
    faker.random.seed()
    joining_char = faker.random_element(elements=[".", "-", "_", ""])
    email_local_part = f"{joining_char.join(name.lower().split(' '))}"
    return f"{email_local_part}@{faker.free_email_domain()}"


@pytest.fixture(autouse=True)
def contributor_factory():
    class ContributorFactory:
        @staticmethod
        def create(name, email, commits=None):
            commits = [] if not commits else commits
            contributor = Contributor(
                name=name,
                email=email,
                commits=commits
            )
            return contributor

    return ContributorFactory


@pytest.fixture(autouse=True)
def contributor(contributor_factory, name: str, email: str):
    return contributor_factory.create(name, email)


@pytest.fixture(autouse=True)
def commit_factory():
    class CommitFactory:
        @staticmethod
        def create(faker, repo, binsha=None):
            binsha = str.encode(
                faker.sha1(raw_output=False)[:20]
            ) if not binsha else binsha
            return Commit(
                repo=repo,
                binsha=binsha
            )

    return CommitFactory


@pytest.fixture(autouse=True)
def commit(commit_factory, faker, remote_url):
    return commit_factory.create(faker, remote_url)


@pytest.fixture(autouse=True)
def repo_factory():
    class RepoFactory:
        @staticmethod
        def create(dir_path, faker):
            faker.random.seed()

            repo = Repo.init(dir_path, initial_branch=f"{faker.word()}")

            contributor = Contributor(
                name="test-bot",
                email=f"test-bot@{faker.free_email_domain()}",
                commits=[]
            )
            RepoFactory.commit(
                faker=faker,
                dir_path=dir_path,
                contributor=contributor,
                message="repo init"
            )
            logger.debug("Initialised Repo on: {}", dir_path)

            return repo

        @staticmethod
        def commit(faker, dir_path, contributor, message=None, file_name=None):
            message = faker.sentence(nb_words=10) if not message else message
            file_name = f"{faker.word()}.txt" if not file_name else file_name
            repo = Repo(dir_path)

            file_path = Path(dir_path) / file_name
            file_path.write_text(message)

            repo.git.add(file_path)
            repo.git.commit("-m", message, author=str(contributor))

            logger.debug(
                "Committed new file '{}' with message: '{}'",
                file_name,
                message
            )

            return repo.head.commit

    return RepoFactory


@pytest.fixture(autouse=True)
def repo(faker, tmp_path_factory, repo_factory):
    tmp_dir = tmp_path_factory.mktemp("data")
    return repo_factory.create(tmp_dir, faker)
