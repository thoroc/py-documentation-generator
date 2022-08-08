from pathlib import Path

from src.models import MissingModuleFilesException
from src.models.local_modules import LocalModule


class ModuleDataProvider:
    BLACKLISTED_DIRS = [
        "__pycache__",
    ]

    BLACKLISTED_FILES = [
        ".DS_Store",
    ]

    def __get_files(self, node: Path, show_empty: bool = False):
        """Get all files in the current directory"""
        files = sorted([n for n in node.glob("*.py") if n.is_file()])

        if len(files) < 1:
            raise MissingModuleFilesException(f'No source files found in "{node}". Are you sure this is a module?')

        if "__init__.py" not in [f.name for f in files]:
            raise MissingModuleFilesException(f'No __init__.py found in "{node}". Are you sure this is a module?')

        if show_empty:
            return [n for n in files if n.stat().st_size > 0]

        return files

    def __walk(self, root: Path, show_empty: bool = False):
        """Walk through directories

        Args:
            root (Path): Root directory
            show_empty (bool): Show empty files

        Returns:
            Dict: JSON representation of node
        """
        modules = {}

        for node in sorted(root.iterdir()):

            if node.is_dir() and node.name not in self.BLACKLISTED_DIRS:
                # Check if directory is a module
                leafs = self.__get_files(node, show_empty)

                if "__init__.py" in [n.name for n in leafs]:
                    modules[node.name] = {
                        "type": "package",
                        "data": self.__walk(node),
                    }

            if node.is_file() and node.stat().st_size > 0:
                modules[node.name] = {
                    "type": "module",
                    "data": LocalModule.from_path(node),
                }

        return modules

    def serialize(self, root: Path, show_empty: bool = False):
        """Serialize package data.

        Args:
            root (Path): Root directory
            show_empty (bool): Show empty files

        Returns:
            Dict: JSON representation of package
        """
        return {
            root.name: {
                "type": "package",
                "data": self.__walk(root, show_empty),
            }
        }
