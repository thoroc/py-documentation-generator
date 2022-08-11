from loguru import logger
from src.models.contributor_manager import ContributorManager


def test__get_contrinutor_found(faker, fake_personalia, fake_local_repo):
    # Arrange
    manager = ContributorManager(
        repo_path=fake_local_repo
    )

    logger.info(manager)

    # Act
    manager._get_contributor(
        name=fake_personalia.name,
        email=fake_personalia.email
    )

    # Assert
    assert False


def test__get_contributor_not_found():
    # Arrange

    # Act

    # Assert
    assert False
