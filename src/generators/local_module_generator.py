from pathlib import Path
import pandas as pd
from loguru import logger

from src.generators.documentation_generator import DocumentationGenerator
from src.models import MissingPackageException
from src.models.module_data_provider import ModuleDataProvider


class LocalModuleGenerator(DocumentationGenerator):
    TYPE_PACKAGE = "package"
    TYPE_MODULE = "module"

    _data_provider = ModuleDataProvider()

    def __modules_to_dataframe(self, modules: list):
        logger.debug(f"MODULES: {modules}")

        if not modules:
            return pd.DataFrame()

        columns = [key[1:] for key in list(modules[0].keys())]
        data = []

        for module in modules:
            values = []

            for value in list(module.values()):
                if isinstance(value, list):
                    values.append(', '.join(value))
                else:
                    values.append(value)

            data.append(values)

        dataframe = pd.DataFrame(data, columns=columns)
        dataframe[columns[0]] = dataframe[columns[0]
                                          ].str.replace("__", r"\_\_")

        return dataframe.to_markdown(index=False)

    def __unwrap(self, nodes: dict, depth: int = 1):
        content = ""

        if isinstance(nodes, dict):
            modules = []

            for key, value in nodes.get("data").items():
                if value.get("type") == self.TYPE_MODULE:
                    modules.append(value.get("data"))

            content += f"{self.__modules_to_dataframe(modules)}\n\n\n"

            for key, value in nodes.get("data").items():
                if value.get("type") == self.TYPE_PACKAGE:
                    content += f"{'#' * (depth + 1)} {key}\n\n"
                    content += self.__unwrap(value, depth + 1)

        return content

    @logger.catch()
    def _get_content(self):
        content = ""

        # logger.info(f"DATA: {self._data}")

        for section, nodes in self._data.items():
            logger.info(f"Object: {section}")

            content += f"# {section}\n\n"
            content += self.__unwrap(nodes)

        return content

    @ logger.catch()
    def _get_data(self):
        cwd = Path(self._source_dir).resolve()
        data = self._data_provider.serialize(cwd)

        if not data:
            raise MissingPackageException("No local modules found")

        return data
