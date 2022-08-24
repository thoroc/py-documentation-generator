from pathlib import Path
import pytest
from loguru import logger
from git import Repo
from src.models.contributor import Contributor
from src.models.contributor_manager import ContributorManager


def test__get_contrinutor_found(faker, tmp_path_factory):
    # Arrange
    contributor = faker.contributor()

    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)
    faker.commit(dir_path=tmp_dir, contributor=contributor)

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


def test__get_contributor_not_found(faker, repo: Repo):
    # Arrange
    contributor = faker.contributor()

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


def test__init_contributors(faker, tmp_path_factory):
    # Arrange
    contributor = faker.contributor()
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)
    faker.commit(dir_path=tmp_dir, contributor=contributor)

    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )
    # Act
    sut = manager._contributors

    # Assert
    assert len(sut) == 2
    for item in sut:
        assert isinstance(item, Contributor)


def test__init_contributors_excluded(
    faker,
    name_factory,
    email_factory,
    tmp_path_factory
):
    # Arrange
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)

    included_name = name_factory.create(faker)
    included_email = email_factory.create(faker, included_name)
    included_contributor = faker.contributor(
        included_name,
        included_email
    )

    faker.commit(dir_path=tmp_dir, contributor=included_contributor)

    excluded_name = name_factory.create(faker)
    excluded_email = email_factory.create(faker, excluded_name)
    excluded_contributor = faker.contributor(
        excluded_name,
        excluded_email
    )

    faker.commit(dir_path=tmp_dir, contributor=excluded_contributor)

    # Act
    manager = ContributorManager(
        repo_path=repo.working_tree_dir,
        exclude=[excluded_email]
    )
    sut = manager._contributors

    # Assert
    assert len(sut) == 2
    for item in sut:
        assert isinstance(item, Contributor)
