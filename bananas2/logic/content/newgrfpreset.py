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

import re

PAT_HEADER = re.compile("\[preset-(.*)]\s*$")
PAT_LINE = re.compile("([0-9A-Fa-f]{8})\|([0-9A-Fa-f]{32})\|(.*[/\\\\])?([^/\\\\]*)=([0-9 ]*)$")

class NewGRFPreset:
    """
    NewGRF preset meta data

    @ivar name: Name of preset
    @type name: C{str}

    @ivar content: List of referenced NewGRF as (grf-id, md5sum, filename, parameters)
    @type content: C{list} of (C{int}, C{str}, C{str}, C{list} of C{int})
    """

    def __init__(self):
        self.name = None
        self.content = []

    def read(self, file):
        """
        Read NewGRF preset

        @param file: File to read
        @type file: File-like object

        @return: True on success.
        @rtype: C{bool}
        """
        try:
            has_header = False
            for l in file:
                l = l.strip()
                if len(l) == 0 or l[0] == "#":
                    continue
                if has_header:
                    m = PAT_LINE.match(l)
                    if m:
                        self.content.append((int(m.group(1), 16), m.group(2), m.group(4).strip(), [int(p) for p in m.group(5).split()]))
                    else:
                        raise Exception("Invalid preset content")
                else:
                    m = PAT_HEADER.match(l)
                    if m:
                        has_header = True
                        self.name = m.group(1)
                    else:
                        raise Exception("Invalid preset header")
        except Exception as e:
            print(e)
            return False
        finally:
            file.close()

        return True

    def write(self, file):
        """
        Write NewGRF preset, properly normalised

        @param file: File to write
        @type file: File-like object

        @return: True on success.
        @rtype: C{bool}
        """
        try:
            if self.name:
                if self.name.find("\n") >= 0:
                    raise Exception("Invalid preset name")
                file.write("[preset-{}]\n".format(self.name))
                for i in self.content:
                    if i[2].find("\n") >= 0:
                        raise Exception("Invalid preset name")
                    pars = " ".join(str(p) for p in i[3])
                    if len(pars) > 0:
                        pars = " " + pars
                    file.write("{:08X}|{}|{} ={}\n".format(i[0], i[1], i[2], pars))
                return True
        except Exception as e:
            print(e)
        return False
