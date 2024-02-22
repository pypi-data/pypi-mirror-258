import logging
import re

from typing_extensions import Any, Callable, Generic, Type, TypeVar

_IDENTIFIER = re.compile("^[a-z_][a-z0-9_]*$", re.I)

T = TypeVar("T", logging.Formatter, logging.Filter, logging.Handler)


class InjectFactory(Generic[T]):
    def __init__(
        self, klass: Type[T], factory: Callable[[Type[T], dict, dict, Any], T]
    ):
        self.__klass = klass
        self.__factory = factory
        setattr(self, "__proxy_class__", self.__klass)

    def new(self, config: dict, namespace: dict, converter) -> T:
        return self.__factory(self.__klass, config, namespace, converter)


def get_classpath(obj: Any) -> str:
    if hasattr(obj, "__proxy_class__"):
        klass = obj.__proxy_class__
    elif not isinstance(obj, type):
        klass = obj.__class__
    else:
        klass = obj

    module = klass.__module__
    if module == "builtins":
        return klass.__qualname__
    return module + "." + klass.__qualname__


def get_attrib(obj: Any, key: str, skip_list: bool = True) -> Any:
    if isinstance(obj, list) and not skip_list:
        return obj[int(key)]
    elif isinstance(obj, dict):
        try:
            return obj[int(key)]
        except ValueError:
            return obj[key]
    else:
        return getattr(obj, key)


def valid_kwargs(kwargs: dict) -> dict:
    def _valid_ident(ident):
        _match = _IDENTIFIER.match(ident)
        if not _match:
            raise ValueError(f"Not a valid Python identifier: {ident}")
        return True

    return {key: value for key, value in kwargs.items() if _valid_ident(key)}


def as_tuple(value: Any) -> tuple:
    if isinstance(value, list):
        value = tuple(value)
    return value
