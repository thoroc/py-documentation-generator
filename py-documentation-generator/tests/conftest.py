from pathlib import Path
from random import randint
from git import Repo, Commit
import pytest
from loguru import logger
from faker.providers import BaseProvider
from faker import Faker
from src.models.contributor import Contributor


@pytest.fixture(autouse=True)
def faker_init(faker):
    # fake = Faker("en_GB")
    faker.add_provider(ContributorProvider)
    faker.add_provider(GitProvider)
    seed = randint(10001, 99999)
    faker.seed_instance(seed)


class ContributorProvider(BaseProvider):

    __provider__ = "email_from_name"
    __provider__ = "contributor"
    __provider__ = "dummy_commit"
    __lang__ = "en_GB"

    def email_from_name(self, name):
        joining_char = self.generator.random_element(
            elements=[".", "-", "_", ""])
        email_local_part = f"{joining_char.join(name.lower().split(' '))}"

        return f"{email_local_part}@{self.generator.free_email_domain()}"

    def contributor(self, name=None, email=None, commits=None):
        name = name if name else self.generator.name()
        email = email if email else self.email_from_name(name=name)
        commits = commits if commits else []

        contributor = Contributor(
            name=name,
            email=email,
            commits=commits
        )

        return contributor

    def dummy_commit(self, repo=None, binsha=None):
        repo = repo if repo else f"https://{self.generator.hostname()}/{self.generator.word()}/{self.generator.word()}"
        binsha = binsha if binsha else str.encode(
            self.generator.sha1(raw_output=False)[:20]
        )

        commit = Commit(
            repo=repo,
            binsha=binsha
        )

        return commit


class GitProvider(BaseProvider):

    __provider__ = "commit"
    __provider__ = "repository"
    __lang__ = "en_GB"

    def commit(self, dir_path, contributor, message=None, file_name=None):
        message = self.generator.sentence(
            nb_words=10) if not message else message
        file_name = f"{self.generator.word()}.txt" if not file_name else file_name

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

    def repository(self, dir_path):
        repo = Repo.init(dir_path, initial_branch=f"{self.generator.word()}")

        logger.debug("Initialised Repo on: {}", dir_path)

        contributor = Contributor(
            name="test-bot",
            email=f"test-bot@{self.generator.free_email_domain()}",
            commits=[]
        )

        self.commit(
            dir_path=dir_path,
            contributor=contributor,
            message="repo init",
            file_name="README.md"
        )

        return repo
