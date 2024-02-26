# -*- coding: utf-8 -*-

"""

tests.test_strings

Unit test the strings module


Copyright (C) 2024 Rainer Schwarzbach

This file is part of smdg.

smdg is free software: you can redistribute it and/or modify
it under the terms of the MIT License.

smdg is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the LICENSE file for more details.

"""


from unittest import TestCase

from smdg import strings


class Functions(TestCase):
    """Test the module functions"""

    def test_sanitize_specials(self) -> None:
        """sanitize() function with the SPECIALS regex"""
        for source, expected_result in (
            ("*", "\\*"),
            ("\\", "\\\\"),
            ("_", "\\_"),
            ("[", "\\["),
            ("]", "\\]"),
        ):
            with self.subTest(source=source, expected_result=expected_result):
                self.assertEqual(
                    strings.sanitize(source),
                    strings.SafeString(expected_result),
                )
            #
        #


# vim: fileencoding=utf-8 ts=4 sts=4 sw=4 autoindent expandtab syntax=python:
