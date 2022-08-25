from click.testing import CliRunner
from src.commands.generate_mailmap import generate_mailmap


def test_generate_mailmap(mocker):
    # Arrange
    runner = CliRunner()

    # Act
    result = runner.invoke(generate_mailmap)

    # Assert
    assert result.exit_code == 0
