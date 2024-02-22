# ruff: noqa
from yaml import load, dump

try:
    from yaml import CDumper as Dumper, CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader
