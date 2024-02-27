__version__ = "0.3.0"

from enum import Enum

version = __version__


class FileType(Enum):
    YAML = "YAML"
    XML = "XML"
    JSON = "JSON"
