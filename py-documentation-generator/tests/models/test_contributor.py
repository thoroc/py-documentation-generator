from git import Commit
from src.models.contributors import Contributor


def test_add_new_commit(faker):
    # Arrange
    commit_1 = faker.binary(length=20)
    commit_2 = faker.binary(length=20)
    commit_3 = faker.binary(length=20)
    contributor = Contributor(
        name=faker.name(),
        email=faker.free_email_domain(),
        commits=[commit_1, commit_2, commit_3],
    )

    # Act
    new_commit = Commit(repo="", binsha=faker.binary(length=20))
    contributor.add_commit(new_commit)

    # Assert
    assert new_commit.hexsha in contributor.commits


def test_add_existing_commit(faker):
    # Arrange
    commit_1 = faker.binary(length=20)
    commit_2 = faker.binary(length=20)
    commit_3 = faker.binary(length=20)
    contributor = Contributor(
        name=faker.name(),
        email=faker.free_email_domain(),
        commits=[commit_1, commit_2, commit_3],
    )

    # Act
    existing_commit = Commit(repo="", binsha=commit_3.encode("utf-8"))
    contributor.add_commit(existing_commit)

    # Assert
    assert existing_commit.hexsha in contributor.commits
    assert 3 == len(contributor.commits)
