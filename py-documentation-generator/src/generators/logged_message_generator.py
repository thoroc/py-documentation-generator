import ast
import re
import logging
from pathlib import Path
import pandas as pd
import astor
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
        # skip for func not being an ast.Attribute or value not being an ast.Name
        if not isinstance(node.func, ast.Attribute) or not isinstance(node.func.value, ast.Name):
            return

        # exit when the node is NOT an instance_name of logger
        if node.func.value.id != self.instance_name:
            return

        # exit when the method is invalid or not the one we want
        if self.log_level not in LOG_LEVEL_NANES or node.func.attr != self.log_level.lower():
            return

        i_args = [astor.to_source(arg) for arg in node.args]
        ast.NodeVisitor.generic_visit(self, node)
        self.stats[node.lineno] = self._cleanup_node(i_args)

    @logger.catch()
    def _cleanup_node(self, instance_args: List[str]):
        """ Clean up node

        Args:
            instance_args (List[str]): list of strings found for each instance of the message

        Returns:
            str: cleaned up message
        """
        logger.debug("instance_args=`{}`", instance_args)

        message = instance_args[0]
        arguments = instance_args[1:]

        logger.debug(arguments)

        no_extra_spaces_message = re.sub(
            r"\s+", " ", message.strip("\n\t")
        )
        no_leading_f_message = re.sub(
            r"^f", "", no_extra_spaces_message
        )
        message = re.sub(
            r"\"+", "", no_leading_f_message
        )

        return message, [arg.strip("\n\t") for arg in arguments]


class LoggedMessageDocumentationGenerator:
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
                log_content = self._parse_logs(
                    file_content, instance_name, log_level)
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

        logged_messages = self._extract_logged_message(
            instance_name, log_level)
        data = []

        logger.info("Generating markdown table for {}", instance_name)

        if logged_messages:
            for file, messages in logged_messages.items():
                for lineno, message in messages.items():
                    file_path = self._get_relative_path(file)
                    lineno_link = self._generate_link(
                        lineno, file_path, file, lineno)
                    data.append(
                        [
                            file.name,
                            file_path,
                            lineno_link,
                            f"`{message[0]}`",
                            ",".join(message[1])
                        ]
                    )

            dataframe = pd.DataFrame(
                data, columns=[
                    "file",
                    "path",
                    "lineno",
                    "message",
                    "args"
                ])  # pylint: disable=C0103

            return dataframe.to_markdown(index=False)

        return False
