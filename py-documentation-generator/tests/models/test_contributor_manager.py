from src.models.contributor import Contributor
from src.models.contributor_manager import ContributorManager


def test__get_contrinutor_found(faker, tmp_path_factory):
    # Arrange
    contributor = faker.contributor()

    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)
    faker.commit(dir_path=tmp_dir, contributor=contributor)

    # Act
    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )
    sut: Contributor = manager._get_contributor(
        name=contributor.name,
        email=contributor.email
    )

    # Assert
    assert sut == contributor


def test__get_contributor_not_found(faker, tmp_path_factory):
    # Arrange
    contributor = faker.contributor()
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)

    # Act
    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )
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

    # Act
    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )
    sut = manager._contributors

    # Assert
    assert len(sut) == 2
    for item in sut:
        assert isinstance(item, Contributor)


def test__init_contributors_excluded(faker, tmp_path_factory):
    # Arrange
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)

    included_contributor = faker.contributor()
    faker.commit(dir_path=tmp_dir, contributor=included_contributor)

    excluded_contributor = faker.contributor()
    faker.commit(dir_path=tmp_dir, contributor=excluded_contributor)

    # Act
    manager = ContributorManager(
        repo_path=repo.working_tree_dir,
        exclude=[excluded_contributor.email]
    )
    sut = manager._contributors

    # Assert
    assert len(sut) == 2
    for item in sut:
        assert isinstance(item, Contributor)
