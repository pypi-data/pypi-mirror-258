#!/usr/bin/python3
"""General functions shared between my scripts."""

__version__ = '1.0.0'


def read_file(filename: str):
    """Read contents of file, close, and then return contents."""
    with open(filename, "r", encoding="UTF-8") as _f:
        return _f.read()


def write_file(filename: str, data: str):
    """Write data to file (does not append), and then close."""
    with open(filename, "w", encoding="UTF-8") as _f:
        _f.write(data)
