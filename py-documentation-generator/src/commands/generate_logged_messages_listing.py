import ast
import re
import logging
from pathlib import Path
import sys
import pandas as pd
import astor
import click
from loguru import logger

LOG_LEVEL_NANES = [*list(logging._nameToLevel.keys()), "EXCEPTION"]


class FuncVisitor(ast.NodeVisitor):
    """Analyzes a Python AST tree and look for function calls

    Usage:
        tree = ast.parse(...)
        visitor = FuncVisitor()
        visitor.visit(tree)
    """

    def __init__(
        self,
        instance_name: str,
        log_level: str = logging._levelToName[logging.INFO],
    ):
        self.stats = {}
        self.instance_name = instance_name
        self.log_level = log_level

    def visit_Call(self, node: ast.Call):  # pylint: disable=C0103
        """Called when the visitor visits an ast.Call

        Args:
            node (ast.Call): The node being visited

        Returns:
            None
        """
        # check for func is an ast.Attribute and value is an ast.Name
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            i_object = node.func.value.id
            i_method = node.func.attr
            i_lineno = node.lineno

            # ensuring the node is an instance_name of logger
            if i_object == self.instance_name:
                no_quotes_message = ""
                i_args = []
                # ensuring the method is valid and is the one we want
                if self.log_level in LOG_LEVEL_NANES and i_method == self.log_level.lower():
                    for arg in node.args:
                        i_args.append(astor.to_source(arg))
                    ast.NodeVisitor.generic_visit(self, node)
                    # clean up i_args
                    joined_message = " ".join(i_args)
                    no_extra_spaces_message = re.sub(r"\s+", " ", joined_message.strip("\n\t"))
                    no_leading_f_message = re.sub(r"^f", "", no_extra_spaces_message)
                    no_quotes_message = re.sub(r"\"+", "", no_leading_f_message)

                    self.stats[i_lineno] = no_quotes_message


class DocumentationGenerator:
    """Generate documentation for logged messages in a project's source code.

    Usage:
        instance_name = "logger"
        log_level = "INFO"
        generator = DocumentationGenerator(source_dir="src", base_url="http://localhost:8000")
        generator.generate(instance_name, log_level)
    """

    def __init__(self, source_dir: str, base_url: str):
        self.source_dir = source_dir
        self.base_url = base_url
        self.local_dir = Path(Path.cwd(), source_dir)

    def _parse_logs(
        self,
        source_code: str,
        instance_name: str,
        log_level: str = LOG_LEVEL_NANES[0],
    ):
        """Parse all logged messages in a source code.

        Args:
            source_code (str): the source code to search
            instance_name (str): the instance name to filter the found logged messages
            log_level (str): the level to filter the found logged messages

        Returns:
            dict: a dictionary of logged messages
        """
        tree = ast.parse(source_code)
        visitor = FuncVisitor(instance_name, log_level)
        visitor.visit(tree)

        return visitor.stats

    def _get_relative_path(self, path: Path):
        """Get the relative path of a path.

        Args:
          path (Path): the path to get the relative path for

        Returns:
          str: relative path
        """
        relative_path = path.parent.relative_to(self.local_dir)
        return str(relative_path) if str(relative_path) != "." else "root"

    def _extract_logged_message(self, instance_name: str, log_level: str):
        """Extract all logged messages from the project's source files.

        Args:
          instance_name (str): the instance name to filter the found logged messages
          log_level (str): the level to filter the found logged messages

        Returns:
          dict: object with key:value pairs of logged messages
        """
        logged_messages = {}

        logger.info("Processing level: {}", log_level)

        for file in self.local_dir.rglob("*.py"):
            with open(file, "r") as file_buffer:
                file_content = file_buffer.read()
                log_content = self._parse_logs(file_content, instance_name, log_level)
                if log_content:
                    logged_messages[file] = log_content

        return logged_messages

    def _generate_link(self, text: str, file_path: str, file: Path, lineno: int):
        """Generate link to a source file.

        Args:
          text (str): the text to link to
          file_path (str): the path to the file
          file (Path): the file to link to
          lineno (int): the line number to link to

        Returns:
          str: the link to the file
        """
        parent_dir = "" if file_path == "root" else f"/{file_path}"
        url = f"{self.base_url}/{str(self.source_dir)}{parent_dir}/{file.name}#lines-{lineno}"
        return f"[{text}]({url})"

    def generate_md(self, instance_name: str, log_level: str):
        """Get the content of the markdown table.

        Args:
          instance_name (str): the instance name to filter the found logged messages
          log_level (str): the level to filter the found logged messages

        Returns:
          str: markdown table content
        """

        logged_messages = self._extract_logged_message(instance_name, log_level)
        data = []

        logger.info("Generating markdown table for {}", instance_name)

        if logged_messages:
            for file, messages in logged_messages.items():
                for lineno, message in messages.items():
                    file_path = self._get_relative_path(file)
                    lineno_link = self._generate_link(lineno, file_path, file, lineno)
                    data.append([file.name, file_path, lineno_link, f"`{message}`"])

            dataframe = pd.DataFrame(data, columns=["file", "path", "lineno", "message"])  # pylint: disable=C0103

            return dataframe.to_markdown(index=False)

        return False


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

    generator = DocumentationGenerator(source_dir, url)

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
