from __future__ import annotations
from pathlib import Path
from git import Repo
from loguru import logger
from .contributors import Contributor


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

            contributor: Contributor = self._get_contributor(
                author_name, author_email)

            if author_email not in self._exclude:
                # check if we have a contributor with the same name and email
                if contributor:
                    logger.debug("Found existing contributor={}", contributor)
                    contributor.add_commit(commit)
                else:
                    contributor = Contributor(
                        author_name, author_email, [commit_hash])
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
                logger.debug(
                    "Writing mailmap entry for contributor={}", contributor)
                file_buffer.write(f"{contributor}\n")
