import click
from src.commands.generate_mailmap import generate_mailmap


@click.group()
def main():
    """Demo"""


if __name__ == '__main__':
    main.add_command(generate_mailmap)
    main()
