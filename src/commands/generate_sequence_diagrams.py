import ast
from pathlib import Path
import sys
from typing import Dict, List, Union
from pip._internal.operations import freeze
import pkg_resources
import click
from isort.stdlibs.py37 import stdlib
from loguru import logger


class Visitor(ast.NodeVisitor):
    imports = []
    imports_from = {}

    def visit_Import(self, node):  # pylint: disable=C0103
        """ Collect all imports """
        for alias in node.names:
            logger.info(f"imported module found: {alias.name}")
            logger.debug(ast.dump(node))
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):  # pylint: disable=C0103
        """ Collect all imports from """
        for alias in node.names:
            logger.info(f"imported from module found: {node.module}")
            logger.debug(ast.dump(node))
            self.imports_from[node.module] = alias.name
        self.generic_visit(node)

    def run(self, code):
        tree = ast.parse(code)
        return self.visit(tree)


def filter_imports(imports: List[str], mask: List[str]):
    return [module for module in imports if module not in mask]


def list_local_modules():
    """ List all local modules """
    local_modules = []
    for module in pkg_resources.working_set:
        local_modules.append({
            "name": module.project_name,
            "version": module.version,
            "path": Path(module.location, module.project_name).resolve(),
            "extra": module.extras,
        })
    return local_modules


def filter_standard_imports(imports: Union[List[str], Dict[str, str]]):
    """ Filter out standard imports """

    dependencies = []
    for module in freeze.freeze():
        dependencies.append(module.split("==")[0])

    if isinstance(imports, list):
        logger.info(f"\n{len(imports)} imports found\n")
        result = []
        for module in imports:
            if module not in stdlib and module not in dependencies:
                result.append(module)
        logger.info(f"{len(result)} imports returned\n")
        return result

    logger.info(f"{len(imports)} imports found\n")
    result = {}
    for key, value in imports.items():
        module = value.split(".")[0]
        if module not in stdlib and module not in dependencies:
            result[key] = value

    logger.info(f"{len(result)} imports returned\n")
    return result


@click.command()
@click.option(
    "-f",
    "--input-file",
    default=Path("main.py"),
    prompt="Please enter the path to the root file to analyse.",
    type=click.Path(exists=True),
    show_default=True
)
@click.option(
    "-o",
    "--output-file",
    default=Path("docs/sequence.png"),
    prompt="Please enter the path to output file.",
    type=click.Path(exists=False),
    show_default=True
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Enable debug mode. Prints debug messages to the console.",
)
def generate_sequence_diagrams(input_file: Union[str, None], output_file: Union[str, None], debug: bool):
    if not debug:
        # default loguru level is DEBUG
        logger.remove()
        logger.add(sys.stderr, level="INFO")

    logger.info(f"Generating sequence diagrams for {input_file}")

    visitor = Visitor()
    visitor.run(Path(input_file).read_text())

    imports = visitor.imports
    imports_from = visitor.imports_from

    logger.info(f"Imports [{len(imports)}]: {imports}")
    logger.info(f"ImportsFrom: [{len(imports_from)}]: {imports_from}")

    dependencies = [module.split("=")[0] for module in freeze.freeze()]

    logger.info(f"Dependencies [{len(dependencies)}]: {dependencies}")

    mask = [*dependencies, *stdlib]

    # check in imports the one that are not from the standard library or from the requirements
    cleaned_imports = filter_imports(imports, mask)

    import_from_modules = [module.split(".")[0]
                           for module in imports_from.keys()]
    # check in imports_from the one that are not from the standard library or from the requirements
    cleaned_imports_from = filter_imports(import_from_modules, mask)

    logger.info(f"Cleaned Imports [{len(cleaned_imports)}]: {cleaned_imports}")
    logger.info(
        f"Cleaned ImportsFrom [{len(cleaned_imports_from)}]: {cleaned_imports_from}")
    logger.info(f"Saving to {output_file}")


if __name__ == "__main__":
    # test_file: str = Path("main.py").resolve()
    # output_file: str = Path("docs/diagrams/main.png").resolve()
    # generate_diagrams(test_file, output_file)
    logger.level("DEBUG", color="<magenta>")
    generate_sequence_diagrams()
