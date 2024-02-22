import copy
import importlib
import logging
import re

from typing_extensions import (
    Any,
    Callable,
    Mapping,
    MutableMapping,
    Optional,
    Type,
    Union,
)

from logx.types import WithFactory
from logx.utils.factories import make_filter, make_formatter, make_handler
from logx.utils.helpers import InjectFactory, get_attrib, get_classpath


class Configurator:
    _WORD_PATTERN = re.compile(r"^\s*(\w+)\s*")
    _INDEX_PATTERN = re.compile(r"^\[\s*(\w+)\s*\]\s*")
    _CONVERT_PATTERN = re.compile(r"^(?P<prefix>[a-z]+)://(?P<suffix>.*)$")

    def __init__(self):
        self.__formatters: MutableMapping[str, WithFactory[logging.Formatter]] = {}
        self.__filters: MutableMapping[str, WithFactory[logging.Filter]] = {}
        self.__handlers: MutableMapping[str, WithFactory[logging.Handler]] = {}
        self.__default_formatter: Optional[str] = None
        self.__default_filter: Optional[str] = None
        self.__converters: Mapping[str, Callable[[Any, str], Any]] = {
            "cfg": self._convert_cfg,
            "ext": self._convert_ext,
        }

    # Converter
    def _convert_cfg(self, obj: Any, path: str) -> Any:
        if len(path) == 0:
            return obj

        if path.startswith("."):
            return self._convert_cfg(obj, path[1:])

        attr_match = self._WORD_PATTERN.match(path)
        if attr_match is not None:
            attribute = attr_match.groups()[0]
            newpath = path[attr_match.end() :]
            newobj = get_attrib(obj, attribute, skip_list=True)
            return self._convert_cfg(newobj, newpath)

        idx_match = self._INDEX_PATTERN.match(path)
        if idx_match is not None:
            idx = idx_match.groups()[0]
            newpath = path[idx_match.end() :]
            newobj = get_attrib(obj, idx, skip_list=False)
            return self._convert_cfg(newobj, newpath)

        return obj

    def _convert_ext(self, namespace: dict, value: str) -> Any:
        module, path = value.split(".", 1)
        obj = importlib.import_module(module)
        for frag in path.split("."):
            obj = getattr(obj, frag)
        return obj

    def convert(self, value: Any, namespace: dict) -> Any:
        if isinstance(value, list):
            return [self.convert(val, namespace) for val in value]
        elif isinstance(value, tuple):
            return (self.convert(val, namespace) for val in value)
        elif isinstance(value, dict):
            return {key: self.convert(val, namespace) for key, val in value.items()}
        elif not isinstance(value, str):
            return value

        _group = self._CONVERT_PATTERN.match(value)
        if _group is not None:
            data = _group.groupdict()
            converter = self.__converters.get(data["prefix"], None)
            if converter is None:
                raise ValueError(
                    "Converter was not found for prefix '{}'".format(data["prefix"])
                )
            return converter(namespace, data["suffix"])

        return value

    # Builder
    def add_formatter(
        self,
        klass: Union[WithFactory[logging.Formatter], Type[logging.Formatter]],
        name: Optional[str] = None,
    ):
        if not isinstance(klass, WithFactory):
            klass = InjectFactory(klass, make_formatter)
        if name is None:
            name = get_classpath(klass)

        self.__formatters[name] = klass
        return self

    def add_filter(
        self,
        klass: Union[WithFactory[logging.Filter], Type[logging.Filter]],
        name: Optional[str] = None,
    ):
        if not isinstance(klass, WithFactory):
            klass = InjectFactory(klass, make_filter)
        if name is None:
            name = get_classpath(klass)

        self.__filters[name] = klass
        return self

    def add_handler(
        self,
        klass: Union[WithFactory[logging.Handler], Type[logging.Handler]],
        name: Optional[str] = None,
    ):
        if not isinstance(klass, WithFactory):
            klass = InjectFactory(klass, make_handler)
        if name is None:
            name = get_classpath(klass)

        self.__handlers[name] = klass
        return self

    def set_default_formatter(self, name: str):
        self.__default_formatter = name
        return self

    def set_default_filter(self, name: str):
        self.__default_filter = name
        return self

    # Config
    def _configure_item(
        self,
        __dict: Mapping[str, WithFactory[Any]],
        config: dict,
        namespace: dict,
        default: Optional[str] = None,
    ):
        cname = config.pop("()", config.pop("class", default))
        if cname is None:
            raise ValueError("Class required")

        factory = __dict[cname]
        item = factory.new(self.convert(config, namespace), namespace, self)
        return item

    def _configure_logger(
        self,
        config: dict,
        namespace: dict,
        name: Optional[str] = None,
        disabled: bool = False,
    ):
        level = config.get("level", None)
        propagate = config.get("propagate", None)

        filters = [
            self._convert_cfg(namespace, f"filters.{name}")
            for name in config.get("filters", [])
        ]

        handlers = [
            self._convert_cfg(namespace, f"handlers.{name}")
            for name in config.get("handlers", [])
        ]

        logger = logging.getLogger(name)
        logger.disabled = disabled
        if level is not None:
            logger.setLevel(logging.getLevelName(level))

        if propagate is not None and name is not None:
            logger.propagate = propagate

        for _filter in filters:
            if isinstance(_filter, logging.Filter):
                logger.addFilter(_filter)

        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        for handler in handlers:
            if isinstance(handler, logging.Handler):
                logger.addHandler(handler)

        return logger

    def configure(self, config: dict) -> None:
        namespace = copy.deepcopy(config)

        # Configure Formatters
        namespace["formatters"] = namespace.get("formatters", {})
        for name, cfg in config.get("formatters", {}).items():
            namespace["formatters"][name] = self._configure_item(
                self.__formatters, cfg, namespace, self.__default_formatter
            )

        # Configure Filters
        namespace["filters"] = namespace.get("filters", {})
        for name, cfg in config.get("filters", {}).items():
            namespace["filters"][name] = self._configure_item(
                self.__filters, cfg, namespace, self.__default_filter
            )

        # Configure Handlers
        namespace["handlers"] = namespace.get("handlers", {})
        for name, cfg in config.get("handlers", {}).items():
            namespace["handlers"][name] = self._configure_item(
                self.__handlers, cfg, namespace, None
            )

        # Configure Loggers
        disable_existing = config.get("disable_existing_loggers", False)
        for name in logging.root.manager.loggerDict.keys():
            self._configure_logger({}, namespace, name=name, disabled=disable_existing)

        for name, cfg in config.get("loggers", {}).items():
            if "loggers" not in namespace:
                namespace["loggers"] = {}
            namespace["loggers"][name] = self._configure_logger(cfg, namespace, name)

        if "root" in config:
            namespace["root"] = self._configure_logger(config["root"], namespace)
