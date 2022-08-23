from pathlib import Path
import pytest
from loguru import logger
from git import Repo
from src.models.contributor import Contributor
from src.models.contributor_manager import ContributorManager


def test__get_contrinutor_found(faker, contributor: Contributor, local_repo: Repo):
    # Arrange
    file_to_commit = Path(local_repo.working_tree_dir) / "test.txt"
    file_to_commit.write_text(faker.sentence(nb_words=10))
    local_repo.git.add(str(file_to_commit))
    local_repo.git.commit(
        "-m", "test commit", author=str(contributor)
    )

    for item in Path(local_repo.working_tree_dir).iterdir():
        logger.debug(item)

    manager = ContributorManager(
        repo_path=local_repo.working_tree_dir
    )

    # Act
    sut: Contributor = manager._get_contributor(
        name=contributor.name,
        email=contributor.email
    )

    # Assert
    assert sut.name == contributor.name
    assert sut.email == contributor.email


def test__get_contributor_not_found(contributor: Contributor, local_repo: Repo):
    # Arrange
    manager = ContributorManager(
        repo_path=local_repo.working_tree_dir
    )

    # pytest.set_trace()

    logger.debug("local_repo: {}", local_repo.working_tree_dir)

    for item in Path(local_repo.working_tree_dir).iterdir():
        logger.debug(item)

    commits = list(local_repo.iter_commits("HEAD"))

    logger.warning("Found a total of {} commits", len(commits))
    for commit in commits:
        logger.debug("Commit: {} by Author: {}", commit, commit.author)

    # Act
    sut: Contributor = manager._get_contributor(
        name=contributor.name,
        email=contributor.email
    )

    # Assert
    assert sut is None
