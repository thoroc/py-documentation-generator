from git import Commit
from src.models.contributor import Contributor


def test_one_commit(faker, remove_url, contributor: Contributor):
    # Arrange
    commit = Commit(
        repo=remove_url,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )

    # Act
    contributor.add_commit(commit)

    # Assert
    assert commit == contributor.commits[0]


def test_add_new_commit(faker, remove_url, contributor: Contributor):
    # Arrange
    existing_commits = [
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        )
    ]
    contributor._commits = existing_commits

    # Act
    new_commit = Commit(
        repo=remove_url,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    contributor.add_commit(new_commit)

    # Assert
    assert new_commit in contributor.commits


def test_add_existing_commit(faker, remove_url, contributor: Contributor):
    # Arrange
    commit_1 = Commit(
        repo=remove_url,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    commit_2 = Commit(
        repo=remove_url,
        binsha=str.encode(faker.sha1(raw_output=False)[:20])
    )
    binhash_3 = str.encode(faker.sha1(raw_output=False)[:20])
    commit_3 = Commit(repo=remove_url, binsha=binhash_3)
    contributor._commits = [commit_1, commit_2, commit_3]

    # Act
    existing_commit = Commit(repo=remove_url, binsha=binhash_3)
    contributor.add_commit(existing_commit)

    # Assert
    assert existing_commit in contributor.commits
    assert 3 == len(contributor.commits)


def test_add_multiple_commits(faker, remove_url, contributor: Contributor):
    # Arrange
    existing_commits = [
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        )
    ]
    contributor._commits = existing_commits

    # Act
    new_commits = [
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
    ]
    contributor.add_commits(new_commits)

    # Assert
    assert set(new_commits).issubset(contributor.commits)
    assert 6 == len(contributor.commits)


def test_add_multiple_existing_commits(faker, remove_url, contributor: Contributor):
    # Arrange
    existing_commits = [
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        ),
        Commit(
            repo=remove_url,
            binsha=str.encode(faker.sha1(raw_output=False)[:20])
        )
    ]
    contributor._commits = existing_commits

    # Act
    contributor.add_commits(existing_commits)

    # Assert
    assert existing_commits == contributor.commits
    assert 3 == len(contributor.commits)


def test_equivalence(faker, remove_url, contributor: Contributor):
    # Arrange

    # Act
    sut_a = Contributor(
        name=contributor.name,
        email=contributor.email,
        commits=[
            Commit(
                repo=remove_url,
                binsha=str.encode(faker.sha1(raw_output=False)[:20])
            )
        ]
    )
    sut_b = Contributor(
        name=contributor.name,
        email=contributor.email,
        commits=[
            Commit(
                repo=remove_url,
                binsha=str.encode(faker.sha1(raw_output=False)[:20])
            )
        ]
    )

    # Assert
    assert sut_a == sut_b
