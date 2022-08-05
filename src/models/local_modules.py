import ast
import json
from typing import Dict, List, Union
from pathlib import Path


class LocalModule(dict):
    """ Local module """

    def __init__(self, name: str, path: str, module: str, functions: List[str], classes: List[str]):
        self._name = name
        self._path = path
        self._module = module
        self._functions = functions
        self._classes = classes
        dict.__init__(self, **self.__dict__)

    @classmethod
    def from_path(cls, path: Path):
        """ Create a LocalModule object from a path.

        Args:
            path (Path): Path to module

        Returns:
            LocalModule: LocalModule object
        """
        _name = path.name
        _path = str(path.relative_to(Path.cwd()).parent)
        _module = path.parent.name
        _functions = cls.__list_methods(path)
        _classes = cls.__list_classes(path)

        return cls(_name, _path, _module, _functions, _classes)

    @classmethod
    def from_dict(cls, data_dict: Dict[str, Union[str, List[str]]]):
        """ Create a LocalModule object from a dict.

        Args:
            data_dict (Dict[str, Union[str, List[str]]]): containing name, path, module, functions and classes

        Returns:
            LocalModule: LocalModule object
        """
        data = {key.replace("_", ""): value for key,
                value in data_dict.items()}

        return cls(**data)

    @staticmethod
    def __list_methods(node: Path):
        """ List all methods.

        Args:
            node (Path): Path to module

        Returns:
            List[str]: List of methods
        """
        curr_path = Path(node)

        with curr_path.open("rt") as curr_file:
            tree = ast.parse(curr_file.read(), filename=curr_path)
            return [func.name for func in tree.body if isinstance(func, ast.FunctionDef)]

    @staticmethod
    def __list_classes(node: Path):
        """ List all classes.

        Args:
            node (Path): Path to module

        Returns:
            List[str]: List of classes
        """
        curr_path = Path(node)

        with curr_path.open("rt") as curr_file:
            tree = ast.parse(curr_file.read(), filename=curr_path)
            return [node.name for node in tree.body if isinstance(node, ast.ClassDef)]

    def __repr__(self):
        return json.dumps(self.__dict__)
