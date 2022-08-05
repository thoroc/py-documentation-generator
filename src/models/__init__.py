class WrongDataTypeException(Exception):
    """ Data must be a dict """


class MissingOutputFilenameException(Exception):
    """ Missing output filename """


class MissingPackageException(Exception):
    """ Missing package files """


class MissingModuleFilesException(Exception):
    """ Missing module files """
