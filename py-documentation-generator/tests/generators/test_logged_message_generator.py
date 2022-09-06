import pytest
import ast
from pathlib import Path
from loguru import logger

from src.generators.logged_message_generator import FuncVisitor, LoggedMessageDocumentationGenerator


class TestFuncVisitor:

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

    @pytest.mark.parametrize("node", [
        (ast.Call(func=ast.Name(id="foo"))),
        (ast.Call(func=ast.Attribute(value=ast.Attribute()))),
        (ast.Call(func=ast.Attribute(value=ast.Name(id="foo")))),
        (ast.Call(func=ast.Attribute(value=ast.Name(id="logger"), attr="warning")))
    ])
    def test_visit_call_is_false(self, node):
        # Arrange
        visitor = FuncVisitor(instance_name="logger", log_level="INFO")

        # Act
        sut = visitor.visit_Call(node)

        # Assert
        assert sut is False

    @ pytest.mark.parametrize("input, expected", [
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


class TestLoggedMessageDocumentionGenerator:

    def test__parse_logs(self, mocker, tmp_path_factory):
        # Arrange
        cwd = mocker.patch.object(Path, "cwd")
        cwd.return_value = tmp_path_factory.mktemp("data")
        gen = LoggedMessageDocumentationGenerator(
            source_dir="py-documentation-generator/src",
            base_url="https://github.com/thoroc/py-documentation-generator"
        )
        # Act
        sut = gen._parse_logs(source_code="", instance_name="logger")

        # Assert
        assert isinstance(sut, dict)
        assert sut == {}

    @pytest.mark.parametrize("log_level, log_func", [
        ("DEBUG", "debug"),
        ("INFO", "info"),
        (None, "critical"),
        ("WARNING", "warning"),
        ("ERROR", "error"),
        ("CRITICAL", "critical"),
        ("EXCEPTION", "exception"),
    ])
    def test__parse_logs_with_source(self, faker, mocker, tmp_path_factory, log_level, log_func):
        # Arrange
        cwd = mocker.patch.object(Path, "cwd")
        cwd.return_value = tmp_path_factory.mktemp("data")
        gen = LoggedMessageDocumentationGenerator(
            source_dir="py-documentation-generator/src",
            base_url="https://github.com/thoroc/py-documentation-generator"
        )
        message, values = faker.interpolated_string()

        # Act
        source_code = f"""# test code
from loguru import logger

logger.{log_func}("{message}", {values})
        """
        sut = gen._parse_logs(
            source_code=source_code,
            instance_name="logger",
            log_level=log_level
        )

        # Assert
        assert isinstance(sut, dict)
        assert sut == {4: (message, [values])}

    def test__get_relative_path_is_root(self, tmp_path_factory, faker):
        # Arrange
        root_dir = tmp_path_factory.mktemp("data")
        src_dir = Path(root_dir, "src")
        random_dir = Path(src_dir, faker.word())

        gen = LoggedMessageDocumentationGenerator(
            source_dir=src_dir,
            base_url="https://github.com/thoroc/py-documentation-generator"
        )

        # Act
        path = gen._get_relative_path(random_dir)

        # Assert
        assert path == "root"

    def test__get_relative_path_other(self, tmp_path_factory, faker):
        # Arrange
        root_dir = tmp_path_factory.mktemp("data")
        src_dir = Path(root_dir, "src")
        random_dir = Path(src_dir, faker.word(), faker.word())

        gen = LoggedMessageDocumentationGenerator(
            source_dir=src_dir,
            base_url="https://github.com/thoroc/py-documentation-generator"
        )

        # Act
        path = gen._get_relative_path(random_dir)

        # Assert
        assert path != "root"
