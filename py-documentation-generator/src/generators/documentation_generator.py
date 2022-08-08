from abc import ABC, abstractmethod
import json
from pathlib import Path
from loguru import logger


from src.models import WrongDataTypeException, MissingOutputFilenameException


class DocumentationGenerator(ABC):
    def __init__(self, source_dir: str, output_dir: str, output_file_name: str = ""):
        self._source_dir = source_dir
        self._output_dir = output_dir
        self._output_file_name = output_file_name.upper()
        self._data = self._get_data()
        self._content = self._get_content()

    @abstractmethod
    def _get_data(self):
        """Generate data"""
        raise NotImplementedError("_generate() must be implemented")

    @abstractmethod
    def _get_content(self):
        """Transform data"""
        raise NotImplementedError("_transform() must be implemented")

    @logger.catch()
    def _get_output_file_path(self, extension: str):
        """Get output file path"""
        return Path(self._output_dir, f"{self._output_file_name}.{extension}")

    @logger.catch()
    def to_markdown(self):
        """Generate markdown data"""
        if not isinstance(self._data, dict):
            raise WrongDataTypeException("Wrong datatype for {}; dict expected".format(type(self._data)))

        if not self._output_file_name:
            raise MissingOutputFilenameException("output_file_name must be specified")

        output_file = self._get_output_file_path("md")

        if self._content:
            with output_file.open("w") as file_buffer:
                logger.debug("Writing data: {}", self._content)
                logger.debug("to {}", output_file)

                file_buffer.write(self._content)

    @logger.catch()
    def to_json(self):
        """Generate json data"""
        if not isinstance(self._data, dict):
            raise WrongDataTypeException("Wrong datatype for {}; dict expected".format(type(self._data)))

        if not self._output_file_name:
            raise MissingOutputFilenameException("output_file_name must be specified")

        output_file = self._get_output_file_path("json")

        with output_file.open("w") as fbuffer:
            json.dump(self._data, fbuffer, indent=4)
