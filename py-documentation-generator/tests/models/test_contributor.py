def test_one_commit(faker):
    # Arrange
    contributor = faker.contributor()
    commit = faker.dummy_commit()

    # Act
    contributor.add_commit(commit)

    # Assert
    assert commit == contributor.commits[0]


def test_add_new_commit(faker):
    # Arrange
    existing_commits = []
    for _ in range(0, 3):
        existing_commits.append(faker.dummy_commit())

    contributor = faker.contributor()
    contributor._commits = existing_commits

    # Act
    new_commit = faker.dummy_commit()
    contributor.add_commit(new_commit)

    # Assert
    assert new_commit in contributor.commits


def test_add_existing_commit(faker):
    # Arrange
    commit_1 = faker.dummy_commit()
    commit_2 = faker.dummy_commit()
    binhash_3 = str.encode(faker.sha1(raw_output=False)[:20])
    commit_3 = faker.dummy_commit(binsha=binhash_3)
    contributor = faker.contributor()
    contributor._commits = [commit_1, commit_2, commit_3]

    # Act
    existing_commit = faker.dummy_commit(binsha=binhash_3)
    contributor.add_commit(existing_commit)

    # Assert
    assert existing_commit in contributor.commits
    assert 3 == len(contributor.commits)


def test_add_multiple_commits(faker):
    # Arrange
    existing_commits = []
    for _ in range(0, 3):
        existing_commits.append(faker.dummy_commit())
    contributor = faker.contributor()
    contributor._commits = existing_commits

    # Act
    new_commits = []
    for _ in range(0, 3):
        new_commits.append(faker.dummy_commit())
    contributor.add_commits(new_commits)

    # Assert
    assert set(new_commits).issubset(contributor.commits)
    assert 6 == len(contributor.commits)


def test_add_multiple_existing_commits(faker):
    # Arrange
    existing_commits = []
    for _ in range(0, 3):
        existing_commits.append(faker.dummy_commit())
    contributor = faker.contributor()
    contributor._commits = existing_commits

    # Act
    contributor.add_commits(existing_commits)

    # Assert
    assert existing_commits == contributor.commits
    assert 3 == len(contributor.commits)


def test_equivalence(faker):
    # Arrange
    name = faker.family_guys(random=True)
    email = faker.email_from_name(name)

    # Act
    sut_a = faker.contributor(
        name=name,
        email=email,
        commits=[faker.dummy_commit()]
    )
    sut_b = faker.contributor(
        name=name,
        email=email,
        commits=[faker.dummy_commit()]
    )

    # Assert
    assert sut_a == sut_b
