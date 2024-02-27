# ruff: noqa: F401

from importlib.metadata import version as _version

from .pytest_regtest import (
    pytest_addoption,
    pytest_configure,
    register_converter_post,
    register_converter_pre,
    regtest,
    regtest_all,
)

__version__ = _version(__package__)
