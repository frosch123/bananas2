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

LICENSE_DIR = os.path.abspath("bananas2/data/licenses")

class License:
    """
    Built-in license to choose for a project.

    @ivar name: Abbreviated name
    @type name: C{str}

    @ivar description: Long name
    @type description: C{str}

    @ivar url: URL
    @type url: C{sr}

    @ivar path: Absolute path to license file.
    @type path: C{str}

    @ivar deprecated: Do not offer the license for new projects.
    @type deprecated: C{boolean}
    """

    def __init__(self, name, description, url, filename, deprecated):
        self.name = name
        self.description = description
        self.url = url
        self.path = os.path.join(LICENSE_DIR, filename)
        self.deprecated = deprecated

LICENSE_LIST = [
    License("CC0 1.0",         "Creative Commons Zero v1.0 Universal",                         "https://creativecommons.org/share-your-work/public-domain/cc0", "CC0-v1.0.txt",          False),
    License("CC-BY 3.0",       "Creative Commons Attribution 3.0",                             "https://creativecommons.org/licenses/by/3.0/",                  "CC-BY-v3.0.txt",        True),
    License("CC-BY 4.0",       "Creative Commons Attribution 4.0",                             "https://creativecommons.org/licenses/by/3.0/",                  "CC-BY-v4.0.txt",        False),
    License("CC-BY-SA 3.0",    "Creative Commons Attribution ShareAlike 3.0",                  "https://creativecommons.org/licenses/by-sa/3.0/",               "CC-BY-SA-v3.0.txt",     True),
    License("CC-BY-SA 4.0",    "Creative Commons Attribution ShareAlike 4.0",                  "https://creativecommons.org/licenses/by-sa/4.0/",               "CC-BY-SA-v4.0.txt",     False),
    License("CC-BY-ND 4.0",    "Creative Commons Attribution NoDerivatives 4.0",               "https://creativecommons.org/licenses/by-nd/4.0/",               "CC-BY-ND-v4.0.txt",     False),
    License("CC-BY-NC 4.0",    "Creative Commons Attribution NonCommercial 4.0",               "https://creativecommons.org/licenses/by-nc/4.0/",               "CC-BY-NC-v4.0.txt",     False),
    License("CC-BY-NC-SA 3.0", "Creative Commons Attribution NonCommercial ShareAlike 3.0",    "https://creativecommons.org/licenses/by-nc-sa/3.0/",            "CC-BY-NC-SA-v3.0.txt",  True),
    License("CC-BY-NC-SA 4.0", "Creative Commons Attribution NonCommercial ShareAlike 4.0",    "https://creativecommons.org/licenses/by-nc-sa/4.0/",            "CC-BY-NC-SA-v4.0.txt",  False),
    License("CC-BY-NC-ND 3.0", "Creative Commons Attribution NonCommercial NoDerivatives 3.0", "https://creativecommons.org/licenses/by-nc-nd/3.0/",            "CC-BY-NC-ND-v3.0.txt",  True),
    License("CC-BY-NC-ND 4.0", "Creative Commons Attribution NonCommercial NoDerivatives 4.0", "https://creativecommons.org/licenses/by-nc-nd/4.0/",            "CC-BY-NC-ND-v4.0.txt",  False),
    License("GPL 2.0",         "GNU General Public License v2.0",                              "https://www.gnu.org/licenses/gpl-2.0.html",                     "GPL-v2.0.txt",          False),
    License("GPL 3.0",         "GNU General Public License v3.0",                              "https://www.gnu.org/licenses/gpl-3.0.html",                     "GPL-v3.0.txt",          False),
]

LICENSE_DICT = dict()
for l in LICENSE_LIST:
    LICENSE_DICT[l.name] = l
