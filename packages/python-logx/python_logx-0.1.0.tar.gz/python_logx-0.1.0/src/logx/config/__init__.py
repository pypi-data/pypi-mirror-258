import logging
import logging.handlers
import os
from collections import defaultdict

from typing_extensions import Optional

from logx.config.configurator import Configurator
from logx.config.loaders import JsonLoader, TomlLoader, YamlLoader


def default_configurator() -> Configurator:
    return (
        Configurator()
        .set_default_filter("logging.Filter")
        .set_default_formatter("logging.Formatter")
        .add_filter(logging.Filter)
        .add_formatter(logging.Formatter)
        .add_handler(logging.StreamHandler)
        .add_handler(logging.FileHandler)
        .add_handler(logging.NullHandler)
        .add_handler(logging.handlers.WatchedFileHandler)
        .add_handler(logging.handlers.RotatingFileHandler)
        .add_handler(logging.handlers.TimedRotatingFileHandler)
        .add_handler(logging.handlers.SocketHandler)
        .add_handler(logging.handlers.DatagramHandler)
        .add_handler(logging.handlers.SysLogHandler)
        .add_handler(logging.handlers.NTEventLogHandler)
        .add_handler(logging.handlers.SMTPHandler)
        .add_handler(logging.handlers.MemoryHandler)
        .add_handler(logging.handlers.HTTPHandler)
        .add_handler(logging.handlers.QueueHandler)
    )


def _check_type(filename: str, _type: Optional[str] = None):
    if _type is None:
        _type = os.path.splitext(filename)[1][1:]

    return defaultdict(
        lambda: None,
        {
            "json": "json",
            "yaml": "yaml",
            "yml": "yaml",
            "toml": "toml",
        },
    )[_type]


def from_file(
    filename: str,
    _type: Optional[str] = None,
    configurator: Optional[Configurator] = None,
) -> None:
    if configurator is None:
        configurator = default_configurator()

    _type = _check_type(filename, _type)
    if _type is None:
        raise ValueError("Failed to guess file type")

    loaders = {"json": JsonLoader, "yaml": YamlLoader, "toml": TomlLoader}
    loaders[_type](filename).load(configurator)
