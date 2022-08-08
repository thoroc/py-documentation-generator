from git import Commit
from src.models.contributors import Contributor
from loguru import logger


def test_one_commit(faker, fake_repo):
    # Arrange
    commit = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    name = faker.name()
    contributor = Contributor(
        name=name,
        email=f"{'.'.join(name.lower().split(' '))}@{faker.free_email_domain()}",
        commits=[],
    )

    # Act
    contributor.add_commit(commit)

    # Assert
    assert commit == contributor.commits[0]


def test_add_new_commit(faker, fake_repo):
    # Arrange
    commit_1 = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    commit_2 = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    commit_3 = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    name = faker.name()
    contributor = Contributor(
        name=name,
        email=f"{'.'.join(name.lower().split(' '))}@{faker.free_email_domain()}",
        commits=[commit_1, commit_2, commit_3],
    )

    # Act
    new_commit = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    contributor.add_commit(new_commit)

    # Assert
    assert new_commit in contributor.commits


def test_add_existing_commit(faker, fake_repo):
    # Arrange
    commit_1 = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    commit_2 = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    binhash_3 = str.encode(faker.sha1(raw_output=False)[:20])
    commit_3 = Commit(repo=fake_repo, binsha=binhash_3)
    contributor = Contributor(
        name=faker.name(),
        email=faker.free_email_domain(),
        commits=[commit_1, commit_2, commit_3],
    )

    # Act
    existing_commit = Commit(repo=fake_repo, binsha=binhash_3)
    contributor.add_commit(existing_commit)

    # Assert
    assert existing_commit in contributor.commits
    assert 3 == len(contributor.commits)
