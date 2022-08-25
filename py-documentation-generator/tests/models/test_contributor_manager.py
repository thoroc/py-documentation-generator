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
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)

    # Act
    manager = ContributorManager(
        repo_path=repo.working_tree_dir
    )
    name = faker.name()
    sut: Contributor = manager._get_contributor(
        name=name,
        email=faker.email_from_name(name)
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
    sut = manager.contributors

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
    sut = manager.contributors

    # Assert
    assert len(sut) == 2
    for item in sut:
        assert isinstance(item, Contributor)


def test__init_contributors_exists(faker, tmp_path_factory):
    # Arrange
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)

    contributor = faker.contributor()
    commit_1 = faker.commit(dir_path=tmp_dir, contributor=contributor)
    commit_2 = faker.commit(dir_path=tmp_dir, contributor=contributor)

    # Act
    manager = ContributorManager(repo_path=repo.working_tree_dir)
    sut = manager._get_contributor(contributor.name, contributor.email)

    # Assert
    assert sut in manager.contributors
    assert len(sut.commits) == 2
    # reverse order (git history)
    assert sut.commits == [commit_2, commit_1]


def test__sort_contributors(faker, tmp_path_factory):
    # Arrange
    tmp_dir = tmp_path_factory.mktemp("data")
    repo = faker.repository(dir_path=tmp_dir)

    peter = faker.contributor(name="Peter Griffin")
    faker.commit(dir_path=tmp_dir, contributor=peter)
    lois = faker.contributor(name="Lois Griffin")
    faker.commit(dir_path=tmp_dir, contributor=lois)
    stewie = faker.contributor(name="Stewie Griffin")
    faker.commit(dir_path=tmp_dir, contributor=stewie)
    brian = faker.contributor(name="Brian Griffin")
    faker.commit(dir_path=tmp_dir, contributor=brian)
    meg = faker.contributor(name="Meg Griffin")
    faker.commit(dir_path=tmp_dir, contributor=meg)
    chris = faker.contributor(name="Chris Griffin")
    faker.commit(dir_path=tmp_dir, contributor=chris)

    # Act
    manager = ContributorManager(
        repo_path=repo.working_tree_dir,
        exclude="test-bot@example.com"
    )
    sut = manager.contributors

    # Assert
    # reverse order (git history)
    assert sut == [chris, meg, brian, stewie, lois, peter]
    manager._sort_contributors()
    assert sut == [brian, chris, lois, meg, peter, stewie]
