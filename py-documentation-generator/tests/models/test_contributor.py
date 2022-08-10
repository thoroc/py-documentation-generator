from git import Commit
from src.models.contributors import Contributor
from loguru import logger


def test_one_commit(faker, fake_repo, fake_personalia):
    # Arrange
    commit = Commit(
        repo=fake_repo,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    contributor = Contributor(
        name=fake_personalia.name,
        email=fake_personalia.email,
        commits=[],
    )

    # Act
    contributor.add_commit(commit)

    # Assert
    assert commit == contributor.commits[0]


def test_add_new_commit(faker, fake_repo, fake_personalia):
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
    contributor = Contributor(
        name=fake_personalia.name,
        email=fake_personalia.email,
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


def test_add_existing_commit(faker, fake_repo, fake_personalia):
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
        name=fake_personalia.name,
        email=fake_personalia.email,
        commits=[commit_1, commit_2, commit_3],
    )

    # Act
    existing_commit = Commit(repo=fake_repo, binsha=binhash_3)
    contributor.add_commit(existing_commit)

    # Assert
    assert existing_commit in contributor.commits
    assert 3 == len(contributor.commits)


def test_add_multiple_commits(faker, fake_repo, fake_personalia):
    # Arrange
    existing_commits = [
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        )
    ]
    contributor = Contributor(
        name=fake_personalia.name,
        email=fake_personalia.email,
        commits=existing_commits,
    )

    # Act
    new_commits = [
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
    ]
    contributor.add_commits(new_commits)

    # Assert
    assert set(new_commits).issubset(contributor.commits)
    assert 6 == len(contributor.commits)


def test_add_multiple_existing_commits(faker, fake_repo, fake_personalia):
    # Arrange
    existing_commits = [
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=fake_repo,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        )
    ]
    contributor = Contributor(
        name=fake_personalia.name,
        email=fake_personalia.email,
        commits=existing_commits,
    )

    # Act
    contributor.add_commits(existing_commits)

    # Assert
    assert existing_commits == contributor.commits
    assert 3 == len(contributor.commits)


def test_equivalence(faker, fake_repo, fake_personalia):
    # Arrange

    # Act
    contributor_a = Contributor(
        name=fake_personalia.name,
        email=fake_personalia.email,
        commits=[
            Commit(
                repo=fake_repo,
                binsha=str.encode(faker.sha1(raw_output=False)[:20])
            )
        ]
    )
    contributor_b = Contributor(
        name=fake_personalia.name,
        email=fake_personalia.email,
        commits=[
            Commit(
                repo=fake_repo,
                binsha=str.encode(faker.sha1(raw_output=False)[:20])
            )
        ]
    )

    # Assert
    assert contributor_a == contributor_b
