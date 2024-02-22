# ruff: noqa
try:
    from tomllib import load, loads
except ImportError:
    from tomli import load, loads
