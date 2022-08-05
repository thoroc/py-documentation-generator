from pathlib import Path
import click
from loguru import logger

from src.generators.local_module_generator import LocalModuleGenerator


@click.command()
@click.option(
    "-s",
    "--source-dir",
    default=Path("src"),
    prompt="Please enter the path to the source code to analyse.",
    type=click.Path(exists=True),
    show_default=True
)
@click.option(
    "-o",
    "--output-dir",
    default=Path("docs"),
    prompt="Please enter the path to the documentation.",
    type=click.Path(exists=True),
    show_default=True
)
@click.option(
    "-t",
    "--doc-type",
    type=click.Choice(["json", "md"]),
    default="md"
)
def generate_local_modules_listing(source_dir: str, output_dir: str, doc_type: str):
    logger.info(f"Generating documentation for {source_dir} (recursive)")

    generator = LocalModuleGenerator(source_dir, output_dir, "modules")
    generator.to_json()
    generator.to_markdown()


if __name__ == "__main__":
    generate_local_modules_listing()
