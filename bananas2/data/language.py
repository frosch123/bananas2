"""
This file is part of BaNaNaS2, an Add-on Content Management System for OpenTTD.
Copyright (C) 2018  Christoph Elsenhans

BaNaNaS2 is free software; you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 2.

BaNaNaS2 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details. You should have received a copy of the
GNU General Public License along with BaNaNaS2. If not, see <http://www.gnu.org/licenses/>.
"""

import os.path
import csv

LANGUAGE_FILE = os.path.abspath("bananas2/data/languages.csv")

LANGUAGE_LIST = []
ISOCODE = dict()
GRFLANGID = dict()
FILENAME = dict()

class Language:
    """
    Language definition

    @ivar isocode: Iso code of language
    @type isocode: C{str}

    @ivar grflangid: GRF language id
    @type grflangid: C{int}

    @ivar filename: Language file name without extension
    @type filename: C{str}

    @ivar name: English name
    @type name: C{str}

    @ivar ownname: Native name
    @type ownname: C{str}
    """

    def __init__(self, row):
        self.isocode = row.get('isocode')
        self.grflangid = int(row.get('grflangid'), 0)
        self.filename = row.get('filename')
        self.name = row.get('name')
        self.ownname = row.get('ownname')

with open(LANGUAGE_FILE, newline='') as f:
    for r in csv.DictReader(f):
        lang = Language(r)
        LANGUAGE_LIST.append(lang)
        ISOCODE[lang.isocode] = lang
        GRFLANGID[lang.grflangid] = lang
        FILENAME[lang.filename] = lang

LANGUAGE_LIST.sort(key=lambda l: l.name)
