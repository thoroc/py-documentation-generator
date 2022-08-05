from __future__ import annotations
import sys
from pathlib import Path
import click
from loguru import logger
from ..models.contributor_manager import ContributorManager


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
def generate_mailmap(exclude: tuple, debug: bool):
    if not debug:
        # default loguru level is DEBUG
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    if exclude:
        logger.info("Excluding emails: {}", list(exclude))

    manager = ContributorManager(Path.cwd(), ".mailmap", list(exclude))
    manager.write_mailmap(True)


if __name__ == "__main__":
    generate_mailmap()
