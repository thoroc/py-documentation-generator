from pathlib import Path
import pytest
from loguru import logger
from git import Repo
from src.models.contributor_manager import ContributorManager
from tests.conftest import Author


def test__get_contrinutor_found(faker, author: Author, fake_local_repo: Repo):
    # Arrange
    file_to_commit = Path(fake_local_repo.working_tree_dir) / "test.txt"
    file_to_commit.write_text(faker.sentence(nb_words=10))
    fake_local_repo.git.add(str(file_to_commit))
    fake_local_repo.git.commit(
        "-m", "test commit", author=author.committer
    )

    manager = ContributorManager(
        repo_path=fake_local_repo.working_tree_dir
    )

    # logger.debug("fake_local_repo: {}", fake_local_repo.working_tree_dir)

    # Act
    contributor = manager._get_contributor(
        name=author.name,
        email=author.email
    )

    # Assert
    assert contributor.name == author.name
    assert contributor.email == author.email


def test__get_contributor_not_found(author: Author, fake_local_repo: Repo):
    # Arrange
    manager = ContributorManager(
        repo_path=fake_local_repo.working_tree_dir
    )

    logger.debug("fake_local_repo: {}", fake_local_repo.working_tree_dir)

    for item in Path(fake_local_repo.working_tree_dir).iterdir():
        logger.warning(item)

    commits = list(fake_local_repo.iter_commits("HEAD"))

    logger.warning("Found a total of {} commits", len(commits))
    for commit in commits:
        logger.debug("Commit: {} by Author: {}", commit, commit.author)

    # Act
    contributor = manager._get_contributor(
        name=author.name,
        email=author.email
    )

    # Assert
    assert contributor is None
