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

from PIL import Image

class Heightmap:
    """
    Heightmap meta data

    @ivar greyscale: Image converted to greyscale
    @type greyscale: C{Image}

    @ivar size: Image size
    @type size: (C{int}, C{int})
    """

    def __init__(self):
        self.size = (None, None)

    def read(self, file):
        """
        Read heightmap meta data

        @param file: File to read
        @type file: File-like object

        @return: True on success.
        @rtype: C{bool}
        """

        try:
            im = Image.open(file)
            self.size = im.size
            self.greyscale = im.convert("L")
        except Exception as e:
            print(e)
            return False
        finally:
            file.close()

        return True

    def write(self, file):
        """
        Write heightmap as proper greyscale png

        @param file: File to write
        @type file: File-like object

        @return: True on success.
        @rtype: C{bool}
        """
        try:
            if self.greyscale:
                self.greyscale.save(file, format="png")
                return True
        except Exception as e:
            print(e)
        return False
