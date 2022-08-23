from __future__ import annotations
from pathlib import Path
from typing import List, Union
from git import Repo
from git.exc import InvalidGitRepositoryError
from loguru import logger

from src.models.contributor import Contributor
from src.models import InvalidGitRepositoryException


@logger.catch
class ContributorManager:
    _repo_path: Path
    _repo: Repo
    _mail_map_path: Path
    _contributors: List[Contributor] = []
    _exclude: list = []

    def __init__(self, repo_path: Path, mail_map_file: str = ".mailmap", exclude: Union[List[str], None] = None):
        """Constructor

        Args:
            repo_path (Path): path to the repo
            mail_map_file (str): name for the mailmap file (default: .mailmap)
            exclude (list): list of email to ignore

        Returns:
            ContributorManager: manager with list of Contributor
        """
        self._repo_path = repo_path
        try:
            self._repo = Repo(repo_path)
        except InvalidGitRepositoryError as exc_info:
            raise InvalidGitRepositoryException(
                "Provided Path is not a valid git repository, not .git subdirectory found."
            ) from exc_info
        self._mail_map_path = Path(mail_map_file)
        self._exclude = exclude if exclude else []
        self._init_contributors()

    @property
    def contributors(self):
        """The list of contributors."""
        return self._contributors

    def _get_contributor(self, name: str, email: str):
        """Get a contributor by name and email.

        Args:
            name (str): the contributor's name
            email (str): the contributor's email

        Returns:
            Contributor|None: the contributor found
        """
        logger.info(
            "Found {} contributor(s) to the repo {}",
            len(self._contributors),
            self._repo.working_tree_dir
        )
        for contributor in self._contributors:
            logger.info("Checking contributor={}", contributor)

            if contributor.name == name and contributor.email == email:
                logger.info("Match found for contributor={}", contributor)
                return contributor

        logger.warning(
            "No contributor found for {} <{}>",
            name, email
        )

        return None

    @logger.catch
    def _init_contributors(self):
        """List all contributors found in repo"""
        commits = list(self._repo.iter_commits("HEAD"))
        logger.info(
            "Generating list of contributors from {} commit(s).",
            len(commits)
        )
        for commit in commits:
            contributor_name = commit.author.name
            contributor_email = commit.author.email

            logger.info(
                "Commit: {} created by: {} <{}>",
                commit, contributor_name, contributor_email
            )

            contributor: Contributor = self._get_contributor(
                contributor_name, contributor_email)

            if contributor_email not in self._exclude:
                # check if we have a contributor with the same name and email
                if contributor:
                    logger.info("Found existing contributor={}", contributor)
                    contributor.add_commit(commit)
                else:
                    contributor = Contributor(
                        contributor_name, contributor_email, [commit])
                    logger.info("Found new contributor={}", contributor)
                    self._contributors.append(contributor)

        logger.info("Found {} contributors", len(self._contributors))

    @logger.catch
    def _sort_contributors(self):
        """Sort contributors by name"""
        self._contributors.sort(key=lambda contributor: contributor.name)

    @logger.catch
    def write_mailmap(self, sorted_contributors: bool = False):
        """Write mailmap file"""
        with self._mail_map_path.open("w") as file_buffer:
            logger.info("Writing mailmap file")

            if sorted_contributors:
                self._sort_contributors()

            for contributor in self._contributors:
                logger.debug(
                    "Writing mailmap entry for contributor={}",
                    contributor
                )
                file_buffer.write(f"{contributor}\n")
