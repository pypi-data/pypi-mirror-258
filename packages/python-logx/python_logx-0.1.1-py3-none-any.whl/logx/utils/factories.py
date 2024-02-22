import logging
import logging.handlers

from typing_extensions import Type

from logx.types import Converter
from logx.utils.helpers import as_tuple, valid_kwargs


def make_formatter(
    klass: Type[logging.Formatter], config: dict, namespace: dict, converter: Converter
):
    fmt = config.get("format", None)
    dfmt = config.get("datefmt", None)
    style = config.get("style", "%")
    props = config.pop(".", None)

    if "validate" in config:
        formatter = klass(fmt, dfmt, style, config["validate"])
    else:
        formatter = klass(fmt, dfmt, style)

    if props:
        for name, value in props.items():
            setattr(formatter, name, value)

    return formatter


def make_filter(
    klass: Type[logging.Filter], config: dict, namespace: dict, converter: Converter
):
    props = config.pop(".", None)
    _filter = klass(**valid_kwargs(config))
    if props:
        for name, value in props.items():
            setattr(_filter, name, value)
    return _filter


def _check_special_cases(
    klass: Type[logging.Handler], config: dict, namespace: dict, converter: Converter
):
    if issubclass(klass, logging.handlers.MemoryHandler):
        target = config.pop("target", None)
        if target is not None:
            config["target"] = converter.convert(f"cfg://handlers.{target}", namespace)
    elif issubclass(klass, logging.handlers.SMTPHandler):
        mailhost = config.pop("mailhost", None)
        if mailhost is not None:
            config["mailhost"] = as_tuple(config["mailhost"])
    elif issubclass(klass, logging.handlers.SysLogHandler):
        address = config.pop("address", None)
        if address is not None:
            config["address"] = as_tuple(config["address"])


def make_handler(
    klass: Type[logging.Handler], config: dict, namespace: dict, converter
):
    level = config.pop("level", "INFO")
    props = config.pop(".", None)

    formatter = config.pop("formatter", None)
    if isinstance(formatter, str):
        formatter = converter.convert(f"cfg://formatters.{formatter}", namespace)

    filters = config.pop("filters", None)
    if filters is not None:
        filters = converter.convert(
            [
                f"cfg://filters.{_filter}" if isinstance(_filter, str) else _filter
                for _filter in filters
            ],
            namespace,
        )

    _check_special_cases(klass, config, namespace, converter)
    handler = klass(**valid_kwargs(config))
    if isinstance(formatter, logging.Formatter):
        handler.setFormatter(formatter)
    if level is not None:
        handler.setLevel(logging.getLevelName(level))
    if filters:
        for _filter in filters:
            if isinstance(_filter, logging.Filter):
                handler.addFilter(_filter)
    if props:
        for name, value in props.items():
            setattr(handler, name, value)

    return handler
