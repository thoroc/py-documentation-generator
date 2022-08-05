from __future__ import annotations
import sys
from pathlib import Path
from git import Repo, Commit
import click
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
        """Add a commit hash to the list of commits.

        Args:
            commit (str): The commit hash to add.
        """
        hexsha = commit.hexsha
        if hexsha not in self._commits:
            self._commits.append(hexsha)
            logger.debug(f"Added commit {hexsha} to {self}")

    def add_commits(self, commits: list):
        """Add a list of commits to the list of commits.

        Args:
            commits (list): The list of commits to add.
        """
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
        return (f"{self.__class__.__name__}"
                f"(name={self._name}, email={self._email}, commits={self._commits})")

    def __str__(self):
        return f"{self._name} <{self._email}>"


@logger.catch
class ContributorManager:
    _repo_path: Path
    _repo: Repo
    _mail_map_path: Path
    _contributors: list = []
    _exclude: list = []

    def __init__(self, repo_path: Path, mail_map_file: str, exclude: list):
        self._repo_path = repo_path
        self._repo = Repo(repo_path)
        self._mail_map_path = Path(mail_map_file)
        self._exclude = exclude
        self._list_contributors()

    @property
    def contributors(self):
        """The list of contributors."""
        return self._contributors

    def _get_contributor(self, name: str, email: str):
        """ Get a contributor by name and email """
        for contributor in self._contributors:
            logger.debug("Checking contributor={}", contributor)

            if contributor.name == name and contributor.email == email:
                logger.debug("Match found for contributor={}", contributor)
                return contributor

        return None

    @logger.catch
    def _list_contributors(self):
        logger.info("Generating list of contributors")
        for commit in self._repo.iter_commits():
            author_name = commit.author.name
            author_email = commit.author.email
            commit_hash = commit.hexsha

            contributor: Contributor = self._get_contributor(author_name, author_email)

            if author_email not in self._exclude:
                # check if we have a contributor with the same name and email
                if contributor:
                    logger.debug("Found existing contributor={}", contributor)
                    contributor.add_commit(commit)
                else:
                    contributor = Contributor(author_name, author_email, [commit_hash])
                    logger.debug("Found new contributor={}", contributor)
                    self._contributors.append(contributor)

    @logger.catch
    def _sort_contributors(self):
        """ Sort contributors by name"""
        self._contributors.sort(key=lambda contributor: contributor.name)

    @logger.catch
    def write_mailmap(self, sorted_contributors: bool = False):
        """ Write mailmap file """
        with self._mail_map_path.open("w") as file_buffer:
            logger.info("Writing mailmap file")

            if sorted_contributors:
                self._sort_contributors()

            for contributor in self._contributors:
                logger.debug("Writing mailmap entry for contributor={}", contributor)
                file_buffer.write(f"{contributor}\n")


@click.command()
@click.option(
    "-e",
    "--exclude",
    type=str,
    multiple=True,
    help="email addresses to exclude from the mailmap file.",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Enable debug mode. Prints debug messages to the console.",
)
def main(exclude: tuple, debug: bool):
    if not debug:
        # default loguru level is DEBUG
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    if exclude:
        logger.info("Excluding emails: {}", list(exclude))

    manager = ContributorManager(Path.cwd(), ".mailmap", list(exclude))
    manager.write_mailmap(True)


if __name__ == "__main__":
    main()
