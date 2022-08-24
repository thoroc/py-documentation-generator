from git import Commit
from src.models.contributor import Contributor
from loguru import logger
import pytest


def test_one_commit(faker, commit: Commit):
    # Arrange
    contributor = faker.contributor()

    # Act
    contributor.add_commit(commit)

    # Assert
    assert commit == contributor.commits[0]


def test_add_new_commit(faker, remote_url, commit_factory):
    # Arrange
    existing_commits = []
    for _ in range(0, 3):
        existing_commits.append(
            commit_factory.create(faker=faker, repo=remote_url))

    contributor = faker.contributor()
    contributor._commits = existing_commits

    # Act
    new_commit = commit_factory.create(faker=faker, repo=remote_url)
    contributor.add_commit(new_commit)

    # Assert
    assert new_commit in contributor.commits


def test_add_existing_commit(faker, remote_url, commit_factory):
    # Arrange
    commit_1 = commit_factory.create(faker=faker, repo=remote_url)
    commit_2 = commit_factory.create(faker=faker, repo=remote_url)
    binhash_3 = str.encode(faker.sha1(raw_output=False)[:20])
    commit_3 = commit_factory.create(
        faker=faker, repo=remote_url, binsha=binhash_3
    )
    contributor = faker.contributor()
    contributor._commits = [commit_1, commit_2, commit_3]

    # Act
    existing_commit = commit_factory.create(
        faker, remote_url, binsha=binhash_3)
    contributor.add_commit(existing_commit)

    # Assert
    assert existing_commit in contributor.commits
    assert 3 == len(contributor.commits)


def test_add_multiple_commits(faker, remote_url, commit_factory):
    # Arrange
    existing_commits = []
    for _ in range(0, 3):
        existing_commits.append(
            commit_factory.create(faker=faker, repo=remote_url)
        )
    contributor = faker.contributor()
    contributor._commits = existing_commits

    # Act
    new_commits = []
    for _ in range(0, 3):
        new_commits.append(commit_factory.create(faker=faker, repo=remote_url))
    contributor.add_commits(new_commits)

    # Assert
    assert set(new_commits).issubset(contributor.commits)
    assert 6 == len(contributor.commits)


def test_add_multiple_existing_commits(faker, remote_url, commit_factory):
    # Arrange
    existing_commits = []
    for _ in range(0, 3):
        existing_commits.append(
            commit_factory.create(faker=faker, repo=remote_url))
    contributor = faker.contributor()
    contributor._commits = existing_commits

    # Act
    contributor.add_commits(existing_commits)

    # Assert
    assert existing_commits == contributor.commits
    assert 3 == len(contributor.commits)


def test_equivalence(faker, remote_url, name, email, commit_factory):
    # Arrange

    # Act
    sut_a = faker.contributor(
        name=name,
        email=email,
        commits=[commit_factory.create(faker=faker, repo=remote_url)]
    )
    sut_b = faker.contributor(
        name=name,
        email=email,
        commits=[commit_factory.create(faker=faker, repo=remote_url)]
    )

    # Assert
    assert sut_a == sut_b
