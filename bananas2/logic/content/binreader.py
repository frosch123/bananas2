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

import struct

class BinaryReader:
    """
    Read binary little endian data.

    @ivar file: Underlying file-like object.
    @type file: File-like

    @ivar hash: Hash for all read data.
    @type hash: C{hash}
    """

    def __init__(self, file, hash = None):
        self.file = file
        self.hash = hash

    def attach_hash(self, hash):
        self.hash = hash

    def detach_hash(self):
        self.hash = None

    def read(self, amount):
        b = self.file.read(amount)
        if self.hash:
            self.hash.update(b)
        return b

    def str(self):
        """
        Read zero-terminated string
        """
        result = bytearray()
        while True:
            b = self.read(1)
            if b == b'\0' or b is None:
                break
            else:
                result.extend(b)
        return result

    def skip(self, amount):
        self.read(amount)

    def uint_ext(self):
        """
        Read NewGRF-style extended byte
        """
        b = self.uint8()
        if b == 0xFF:
            b = self.uint16()
        return b

    def int8(self):
        b = self.read(1)
        return struct.unpack("<b", b)[0]

    def uint8(self):
        b = self.read(1)
        return struct.unpack("<B", b)[0]

    def int16(self):
        b = self.read(2)
        return struct.unpack("<h", b)[0]

    def uint16(self):
        b = self.read(2)
        return struct.unpack("<H", b)[0]

    def int32(self):
        b = self.read(4)
        return struct.unpack("<l", b)[0]

    def uint32(self):
        b = self.read(4)
        return struct.unpack("<L", b)[0]

    def int64(self):
        b = self.read(8)
        return struct.unpack("<q", b)[0]

    def uint64(self):
        b = self.read(8)
        return struct.unpack("<Q", b)[0]
