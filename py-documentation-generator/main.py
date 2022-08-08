import click
from src.commands.generate_local_modules_listing import (
    generate_local_modules_listing,
)
from src.commands.generate_logged_messages_listing import (
    generate_logged_messages_listing,
)
from src.commands.generate_mailmap import generate_mailmap


@click.group()
def main():
    """Documentation Generator"""


if __name__ == "__main__":
    main.add_command(generate_mailmap)
    main.add_command(generate_local_modules_listing)
    main.add_command(generate_logged_messages_listing)
    main()
