import logging
from pathlib import Path
import sys
import click
from loguru import logger

from src.generators.logged_message_generator import LoggedMessageDocumentationGenerator

LOG_LEVEL_NANES = [*list(logging._nameToLevel.keys()), "EXCEPTION"]


@click.command()
@click.option(
    "-o",
    "--output_file",
    type=str,
    prompt="Please enter the filename where the documentation will be writen to.",
    default="LOGGED_MESSAGES.md",
    show_default=True,
)
@click.option(
    "-i",
    "--instance_name",
    type=str,
    prompt="Please enter the name of the logging instance_name in your code.",
    default="logger",
    show_default=True,
)
@click.option(
    "-d",
    "--source_dir",
    type=str,
    prompt="Please enter the path to the source code to analyse.",
    default="src",
    show_default=True,
)
@click.option(
    "-u",
    "--url",
    type=str,
    prompt="Please enter the url to the hosted repo.",
    default="https://github.com/thoroc/py-documentation-generator",
    show_default=True,
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Enable debug mode. Prints debug messages to the console.",
)
def generate_logged_messages_listing(
    output_file: str,
    instance_name: str,
    source_dir: str,
    url: str,
    debug: bool,
):
    """Write the logged messages to a markdown file.

    Args:
      output_file (str): the name of the markdown file to write to
      instance_name (str): the instance name to filter the found logged messages
      source_dir (str): the source code directory
      url (str): the url to the bitbucket repository

    Returns:
      None
    """
    if not debug:
        # default loguru level is DEBUG
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    generator = LoggedMessageDocumentationGenerator(source_dir, url)

    output_path = Path(Path.cwd(), "docs", output_file)

    with output_path.open("w") as file_buffer:
        file_buffer.write("# Logs\n\n")

        for level in LOG_LEVEL_NANES:
            table = generator.generate_md(instance_name, level)
            if table:
                logger.info("Writing level: {}", level)
                file_buffer.write(f"## {level}\n\n")
                file_buffer.write(table)
                if level != LOG_LEVEL_NANES[-1]:
                    file_buffer.write("\n\n")

        logger.info("Done writing to file: {}", output_path)


if __name__ == "__main__":
    generate_logged_messages_listing()
