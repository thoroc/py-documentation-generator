import pytest
import ast
from loguru import logger

from src.generators.logged_message_generator import FuncVisitor


class TestFuncVisitor:

    @pytest.mark.skip()
    def test__init__(self):
        # Arrange

        # Act

        # Assert
        assert True

    @pytest.mark.parametrize("log_level, expected", [
        ("DEBUG", "debug"),
        ("INFO", "info"),
        ("WARNING", "warning"),
        ("ERROR", "error"),
        ("CRITICAL", "critical"),
        ("EXCEPTION", "exception"),
    ])
    def test__check_log_level_ok(self, log_level, expected):
        # Arrange
        visitor = FuncVisitor(instance_name="logger", log_level=log_level)

        # Act
        log_level = visitor._check_log_level(log_level)

        # Assert
        assert log_level == expected

    def test__check_log_level_exception(self):
        # Arrange
        visitor = FuncVisitor(instance_name="logger", log_level="INFO")

        # Act
        with pytest.raises(ValueError):
            visitor._check_log_level("foo")

        # Assert
        assert True

    @pytest.mark.parametrize("log_level, node_func_attr", [
        ("DEBUG", "debug"),
        ("INFO", "info"),
        ("WARNING", "warning"),
        ("ERROR", "error"),
        ("CRITICAL", "critical"),
        ("EXCEPTION", "exception"),
    ])
    def test_visit_call(self, faker, log_level, node_func_attr):
        # Arrange
        visitor = FuncVisitor(instance_name="logger", log_level=log_level)
        node = faker.ast_Call("logger", node_func_attr)

        logger.warning(ast.dump(node))

        # Act
        sut = visitor.visit_Call(node)

        # Assert
        assert sut is True

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
