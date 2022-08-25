from pathlib import Path
from random import randint
from git import Repo, Commit
import pytest
from faker.providers import BaseProvider
from src.models.contributor import Contributor


@pytest.fixture(autouse=True)
def faker_init(faker):
    faker.add_provider(CartoonCharactersProvider)
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
        name = name if name else self.generator.family_guys(random=True)
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

        return repo.head.commit

    def repository(self, dir_path):
        repo = Repo.init(dir_path, initial_branch=f"{self.generator.word()}")

        contributor = Contributor(
            name="test-bot",
            email="test-bot@example.com",
            commits=[]
        )

        self.commit(
            dir_path=dir_path,
            contributor=contributor,
            message="repo init",
            file_name="README.md"
        )

        return repo


class CartoonCharactersProvider(BaseProvider):

    __provider__ = "family_guys"

    def family_guys(self, random=False, extended=False):
        griffin_family = [
            "Peter Griffin",
            "Lois Griffin",
            "Chris Griffin",
            "Meg Griffin",
            "Stewie Griffin",
            "Brian Griffin"
        ]
        brown_family = [
            "Cleveland Brown",
            "Loretta Brown",
            "Cleveland Brown Jr.",
            "Donna Tubbs-Brown",
            "Roberta Tubbs",
            "Rallo Tubbs",
        ]
        quagmire_family = [
            "Glenn Quagmire",
            "Crystal Quagmire",
            "Ida Davis",
            "Brenda Quagmire",
            "Gary Quagmire",
            "Anna Lee",
            "Courtney Quagmire"
        ]

        characters = []
        characters.extend(griffin_family)

        if extended:
            characters.extend(brown_family)
            characters.extend(quagmire_family)
        else:
            characters.extend([brown_family[0]])
            characters.extend([quagmire_family[0]])

        if random:
            return self.random_element(elements=characters)

        return characters
