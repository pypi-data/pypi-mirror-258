import json
from abc import ABCMeta, abstractmethod

try:
    from logx.compat import yaml

    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

try:
    from logx.compat import toml

    _HAS_TOML = True
except ImportError:
    _HAS_TOML = False


class _BaseFileLoader(metaclass=ABCMeta):
    def __init__(self, filename: str) -> None:
        self._filename = filename

    @abstractmethod
    def _load(self) -> dict:
        raise NotImplementedError

    def load(self, configurator) -> None:
        configurator.configure(self._load())


class JsonLoader(_BaseFileLoader):
    def _load(self):
        with open(self._filename, "rb") as fp:
            return json.load(fp)


class TomlLoader(_BaseFileLoader):
    if _HAS_TOML:

        def _load(self):  # type: ignore
            with open(self._filename, "rb") as fp:
                return toml.load(fp)
    else:

        def _load(self):
            raise RuntimeError(
                "Python versions prior to 3.11 don't have built-in support for toml. "
                "Make sure to install python-logx[toml]."
            )


class YamlLoader(_BaseFileLoader):
    if _HAS_YAML:

        def _load(self):  # type: ignore
            with open(self._filename, "rb") as fp:
                return yaml.load(fp, yaml.Loader)
    else:

        def _load(self):
            raise RuntimeError(
                "Python doesn't have built-in support for yaml. "
                "Make sure to install python-logx[yaml]."
            )
