"""
This file is part of BaNaNaS2, an Add-on Content Management System for OpenTTD.
Copyright (C) 2018, 2020 The OpenTTD team

BaNaNaS2 is free software; you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 2.

BaNaNaS2 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details. You should have received a copy of the
GNU General Public License along with BaNaNaS2. If not, see <http://www.gnu.org/licenses/>.
"""

import os.path

TOS_DIR = os.path.abspath("bananas2/data/terms")

class TermsOfService:
    """
    Built-in terms to use Bananas

    @ivar version: Version
    @type version: C{str}

    @ivar description: Long name
    @type description: C{str}

    @ivar path: Absolute path to TOS file.
    @type path: C{str}
    """

    def __init__(self, version, description, filename):
        self.version = version
        self.description = description
        self.path = os.path.join(TOS_DIR, filename)

TOS_LIST = [
    TermsOfService("1.2", "Terms of Service 1.2, 2010-01-26", "TOS-v1.0.md"),
]

TOS_DEFAULT = TOS_LIST[-1]

TOS_DICT = dict()
for l in TOS_LIST:
    TOS_DICT[l.version] = l
