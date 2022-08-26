import pytest

from src.generators.logged_message_generator import FuncVisitor


class TestFuncVisitor:

    @pytest.mark.skip()
    def test__init__(self):
        # Arrange

        # Act

        # Assert
        assert True

    @pytest.mark.skip()
    def test_visit_call(self):
        # Arrange

        # Act

        # Assert
        assert True

    @pytest.mark.parametrize("input, expected", [
        ("  message with some  extra spaces   ", "message with some extra spaces"),
        ("  message with leading spaces", "message with leading spaces"),
        ("message with tailing spaces   ", "message with tailing spaces"),
        ("message with line return\n", "message with line return"),
        ("message with extra tab char\n", "message with extra tab char"),
        ("message with double \"quotes\"", "message with double quotes"),
        ("f\"message with string interpolation\"",
         "message with string interpolation"),
    ])
    def test__cleanup_node_message_with_extra_chars(self, input, expected):
        # Arrange
        instance_args = [input, "args"]
        visitor = FuncVisitor("logger")

        # Act
        message, _ = visitor._cleanup_node(instance_args)

        # Assert
        assert message == expected

    def test__cleanup_node_args(self):
        # Arrange
        instance_args = ["message", "args1", "args2\t", "args3\n"]
        visitor = FuncVisitor("logger")

        # Act
        _, arguments = visitor._cleanup_node(instance_args)

        # Assert
        assert arguments == ["args1", "args2", "args3"]
