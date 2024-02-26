# -*- coding: utf-8 -*-

"""

smdg.strings

Source string handling


Copyright (C) 2024 Rainer Schwarzbach

This file is part of smdg.

smdg is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

smdg is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


# import logging

import re

from typing import List, Sequence, Union


#
# Constants
#


BLANK = " "
EQUALS_OP = "="
EMPTY = ""
LF = "\n"
BACKSLASH = "\\"
BACKTICK = "`"
BLOCKQUOTE_PREFIX = "> "
ASTERISK = "*"
POUND = "#"
UNDERLINE = "_"
ARGS_JOINER = ", "
SQUARE_BRACKETS = "[]"

SPECIALS = f"{ASTERISK}{UNDERLINE}{BACKSLASH}{SQUARE_BRACKETS}"
PRX_SPECIALS = re.compile(f"[{re.escape(SPECIALS)}]")
PRX_ASTERISKS_ONLY = re.compile(f"{re.escape(ASTERISK)}")
PRX_UNDERLINES_ONLY = re.compile(f"{UNDERLINE}")
BACKSLASH_ESCAPED_REPLACEMENT = f"{3 * BACKSLASH}g<0>"


#
# Classes
#


class SafeString:
    """A string declared as safe"""

    def __init__(self, source: Union[str, "SafeString"]) -> None:
        """Store the source"""
        if isinstance(source, str):
            self._original = source
        else:
            self._original = str(source)
        #

    def __repr__(self) -> str:
        """String representation"""
        return f"{self.__class__.__name__}({repr(self._original)})"

    def __str__(self) -> str:
        """Source string"""
        return self._original

    def __hash__(self) -> int:
        """Hash over the string representation"""
        return hash(self._original)

    def __contains__(self, item) -> bool:
        """'in' implementation"""
        if isinstance(item, str):
            maybe_contained = item
        else:
            maybe_contained = str(item)
        return maybe_contained in self._original

    def __mul__(self, other) -> "SafeString":
        """Multiplied other times"""
        if isinstance(other, int):
            return SafeString(self._original * other)
        #
        raise ValueError("Can only multiply with integers")

    def __eq__(self, other) -> bool:
        """Equality check"""
        return isinstance(other, SafeString) and str(self) == str(other)

    __imul__ = __mul__
    __rmul__ = __mul__

    def copy(self) -> "SafeString":
        """String representation"""
        return SafeString(self._original)

    def join(self, parts: Sequence["SafeString"]) -> "SafeString":
        """Return a safe joined string"""
        return self.__class__(str(self).join(str(item) for item in parts))

    def splitlines(self) -> List["SafeString"]:
        """Return a list of lines"""
        return [SafeString(line) for line in str(self).splitlines()]


#
# Helper Functions
#


def sanitize(
    source: str,
    pattern: re.Pattern[str] = PRX_SPECIALS,
    replacement: str = BACKSLASH_ESCAPED_REPLACEMENT,
) -> SafeString:
    """Return source with various characters defused"""
    return SafeString(pattern.sub(replacement, source))


def declare_as_safe(source: str) -> SafeString:
    """Return source directly declared as safe"""
    return SafeString(source)


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
