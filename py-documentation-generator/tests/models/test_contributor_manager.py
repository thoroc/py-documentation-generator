from pathlib import Path
import pytest
from loguru import logger
from git import Repo
from src.models.contributor import Contributor
from src.models.contributor_manager import ContributorManager


def test__get_contrinutor_found(faker, contributor: Contributor, repo_factory, tmp_path_factory):
    # Arrange
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = repo_factory.create(tmp_dir, faker)
    repo_factory.commit(faker, tmp_dir, contributor)

    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )

    # Act
    sut: Contributor = manager._get_contributor(
        name=contributor.name,
        email=contributor.email
    )

    # Assert
    assert sut == contributor


def test__get_contributor_not_found(contributor: Contributor, repo: Repo):
    # Arrange
    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )

    logger.debug("repo: {}", repo.working_tree_dir)

    for item in Path(repo.working_tree_dir).iterdir():
        logger.debug(item)

    commits = list(repo.iter_commits("HEAD"))

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


def test__init_contributors(faker, contributor: Contributor, repo_factory, tmp_path_factory):
    # Arrange
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = repo_factory.create(tmp_dir, faker)
    repo_factory.commit(faker, tmp_dir, contributor)

    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )
    # Act
    sut = manager._contributors

    # Assert
    assert len(sut) == 2
    for item in sut:
        assert isinstance(item, Contributor)
