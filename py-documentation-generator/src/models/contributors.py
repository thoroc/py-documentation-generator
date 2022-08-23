from __future__ import annotations
from typing import List
from git import Commit
from loguru import logger


@logger.catch
class Contributor:
    _name: str
    _email: str
    _commits: list

    def __init__(self, name: str, email: str, commits: list):
        self._name = name
        self._email = email
        self._commits = commits

    def add_commit(self, commit: Commit):
        """Add a Commit to the list of existing Commit.

        Args:
            commit (Commit): The commit to add.
        """
        if commit not in self._commits:
            self._commits.append(commit)
            logger.info("Assign commit {} to {}", repr(commit), self)

    def add_commits(self, commits: List[Commit]):
        """Add a list of Commit to the list of existing Commit.

        Args:
            commits (list): The list of Commit to add.
        """
        logger.info("Assigning {} commits", len(commits))
        for commit in commits:
            self.add_commit(commit)

    @property
    def name(self):
        """The name of the contributor."""
        return self._name

    @property
    def email(self):
        """The email of the contributor."""
        return self._email

    @property
    def commits(self):
        """The list of commits."""
        return self._commits

    def __eq__(self, other: Contributor):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self._name, self._email) == (other._name, other._email)

    def __repr__(self):
        return f"{self.__class__.__name__}" f"(name={self._name}, email={self._email}, commits={self._commits})"

    def __str__(self):
        return f"{self._name} <{self._email}>"
