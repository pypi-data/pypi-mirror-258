# python-logx

The Python [logging](https://docs.python.org/3/library/logging.html) module lets developers configure logging using a *json* file or any format convertible to a Python dictionary. While examining the underlying code, I noticed that some parts, like the section dedicated to configuring special logging handlers in [DictConfigurator._configure_handler](https://github.com/python/cpython/blob/113687a8381d6dde179aeede607bcbca5c09d182/Lib/logging/config.py#L741) method, are getting a bit messy. I took this chance to better understand the logging module and try to improve its current implementation. Right now, my focus is on configuration, but I might add more features later on.

## Usage

### Configurator
The `Configurator` class takes a configuration dictionary and creates all the necessary handlers, formatters, filters, and loggers. Unlike the standard logging module, where developers can use built-in handlers without explicit registration, this library follows a different approach:

- All classes required in the configuration need to be registered in the configurator.
- There's no separation between built-in classes and user-defined classes.

Given the common use of built-in handlers, developers can simply use the `default_configurator` function to get a configurator with all the built-in handlers, along with the default classes for formatter and filter.

```python
from logx.config import default_configurator
configurator = default_configurator()
```

## Example
In this example, we'll use the following configuration.

> [!NOTE]
> The configuration schema can be found in the official [logging.config documentation](https://docs.python.org/3/library/logging.config.html#dictionary-schema-details).

```json
// config.json
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "simple": {
            "format": "[{asctime}] {levelname} - ({name}) : {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{"
        },
        "verbose": {
            "format": "[{asctime}] {levelname} - ({name}) - {module}.{funcName} : {message}",
            "style": "{"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "filename": "app.log"
        }
    },
    "loggers": {
        "database": { "level": "DEBUG" },
        "program": { "level": "INFO" }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [ "console", "file" ]
    }
}
```

This configuration contains:
- 2 formatters: *simple* and *verbose*.
- 2 handlers:
    - *console*, directing output to `stdout` using the *simple* formatter.
    - *file*, directing output to a file (app.log) with the *verbose* formatter.
- 2 loggers: *database* and *program*

Additionally, it configures the root logger to use both handlers.

To load this configuration, use the following code:
```python
import json
import logging

from logx.config import default_configurator

configurator = default_configurator()

with open("config.json", "rb") as fp:
    cfg = json.load(fp)

configurator.configure(cfg)

# Now, use the loggers as usual
db_logger = logging.getLogger("database")
prog_logger = logging.getLogger("program")
```