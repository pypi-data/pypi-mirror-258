# -*- coding: utf-8 -*-

"""

smdg.elements

Markdown elements


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

from typing import List, Optional, Set, Union

# local modules

from smdg import strings


#
# Constants
#


SAFE_LF = strings.SafeString(strings.LF)
SAFE_EMPTY = strings.SafeString(strings.EMPTY)
SAFE_BLOCKQUOTE_PREFIX = strings.SafeString(strings.BLOCKQUOTE_PREFIX)
SAFE_BACKTICK = strings.SafeString(strings.BACKTICK)
SAFE_UNDERLINE = strings.SafeString(strings.UNDERLINE)
SAFE_ASTERISK = strings.SafeString(strings.ASTERISK)
SAFE_POUND = strings.SafeString(strings.POUND)
SAFE_INDENT = strings.SafeString(4 * strings.BLANK)


class BaseElement(strings.SafeString):
    """MarkDown base class"""

    def __init__(self, source: Union[str, strings.SafeString]) -> None:
        """Store the defused internal source"""
        if isinstance(source, str):
            defused = strings.sanitize(source)
        else:
            defused = source
        #
        super().__init__(defused)


class InlineElement(BaseElement):
    """Inline element, may not contain newlines"""

    def __init__(self, source: Union[str, strings.SafeString]) -> None:
        """Store the defused internal source"""
        super().__init__(source)
        if strings.LF in self:
            raise ValueError("Inline elements may not contain line feeds")
        #


class CompoundElement(BaseElement):
    """Compound MarkDown Element"""

    joiner: strings.SafeString = SAFE_EMPTY

    def __init__(
        self,
        *sources: Union[str, strings.SafeString],
    ) -> None:
        """Store the parts in a list"""
        self._sources: List[BaseElement] = [
            BaseElement(single_source) for single_source in sources
        ]
        super().__init__(self.joiner.join(self._sources))

    def flattened(self):
        """return an iterator over flattened conntents"""
        for item in self._sources:
            if isinstance(item, CompoundElement):
                for subitem in item.flattened():
                    yield subitem
                #
            else:
                yield item
            #
        #


class CompoundInlineElement(CompoundElement, InlineElement):
    """Compound inline element"""

    def __init__(
        self,
        *sources: Union[str, strings.SafeString],
    ) -> None:
        """Ensure only inline elements are stored"""
        super().__init__(*(InlineElement(item) for item in sources))


class InlineLiteral(CompoundInlineElement):
    """Backticks quoted inline literal"""

    def __init__(
        self, source: Union[str, InlineElement], tripled: bool = False
    ) -> None:
        """Declare the internal source as safe and surround with backticks"""
        # Define single or triple quote
        quote = SAFE_BACKTICK
        if tripled:
            quote = quote * 3
        #
        super().__init__(quote, strings.SafeString(source), quote)


class InlineContainer(CompoundInlineElement):
    """Inline container element"""

    description = "Inline"
    escape_pattern = strings.PRX_SPECIALS
    forbidden_contents: Set[strings.SafeString] = set()

    def __init__(
        self,
        source: Union[str, BaseElement],
        delimiter: strings.SafeString = SAFE_EMPTY,
    ) -> None:
        """Make sure the source contains neither unescaped underlines
        nor any newlines, and prohibit nested italic text
        """
        if isinstance(source, str):
            checked_source: strings.SafeString = strings.sanitize(
                source, pattern=self.escape_pattern
            )
        else:
            if isinstance(source, CompoundElement):
                for item in source.flattened():
                    if item in self.forbidden_contents:
                        raise ValueError(
                            f"{self.description} text may not be nested"
                        )
                    #
                #
            #
            checked_source = source
        #
        super().__init__(delimiter, checked_source, delimiter)


class ItalicText(InlineContainer):
    """Italic text element"""

    description = "Italic"
    escape_pattern = strings.PRX_UNDERLINES_ONLY
    forbidden_contents: Set[strings.SafeString] = {SAFE_UNDERLINE}

    def __init__(self, source: Union[str, BaseElement]) -> None:
        """Make sure the source contains neither unescaped underlines
        nor any newlines, and prohibit nested italic text
        """
        super().__init__(source, delimiter=SAFE_UNDERLINE)


class BoldText(InlineContainer):
    """Italic text element"""

    description = "Bold"
    escape_pattern = strings.PRX_ASTERISKS_ONLY
    forbidden_contents: Set[strings.SafeString] = {
        SAFE_ASTERISK,
        2 * SAFE_ASTERISK,
    }

    def __init__(self, source: Union[str, BaseElement]) -> None:
        """Make sure the source contains neither unescaped asterisks
        nor any newlines, and prohibit nested bold text
        """
        super().__init__(source, delimiter=2 * SAFE_ASTERISK)


class BlockElement(CompoundElement):
    """Block element"""

    joiner: strings.SafeString = SAFE_LF
    prefix: Optional[strings.SafeString] = None

    def __init__(
        self, *source_elements: Union[str, strings.SafeString]
    ) -> None:
        """Store the lines in a CompoundElement"""
        self._source_lines: List[InlineElement] = []
        for element in source_elements:
            for line in element.splitlines():
                if self.prefix is None:
                    self._source_lines.append(InlineElement(line))
                else:
                    self._source_lines.append(
                        CompoundInlineElement(self.prefix, line)
                    )
                #
            #
        #
        super().__init__(*self._source_lines)


class BlockQuote(BlockElement):
    """BlockQuote"""

    prefix = SAFE_BLOCKQUOTE_PREFIX


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
