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

import hashlib
import io
import zlib, lzma
from . import binreader

class PlainFile:
    @staticmethod
    def open(f):
        return f

class ZLibFile:
    @staticmethod
    def open(f):
        return ZLibFile(f)

    def __init__(self, file):
        self.file = file
        self.decompressor = zlib.decompressobj()
        self.uncompressed = bytearray()

    def close(self):
        pass

    def read(self, amount):
        while len(self.uncompressed) < amount:
            new_data = self.file.read(8192)
            if len(new_data) == 0:
                break
            self.uncompressed += self.decompressor.decompress(new_data)

        data = self.uncompressed[0:amount]
        self.uncompressed = self.uncompressed[amount:]
        return data

UNCOMPRESS = {
    b"OTTN": PlainFile,
    b"OTTZ": ZLibFile,
    b"OTTX": lzma,
    #b"OTTD": lzo2,
}

class Savegame:
    """
    Savegame meta data

    @ivar md5sum: md5 checksum of compressed savegame
    @type md5sum: C{hash}

    @ivar savegame_version: Savegame version
    @type savegame_version: C{int}

    @ivar map_size: Map size
    @type map_size: (C{int}, c{int})

    @ivar newgrf: List of NewGRF as (grf-id, md5sum, version, filename)
    @type newgrf: C{list} of (C{int}, C{str}, C{int}, C{str})

    @ivar ai: List of non-random AIs as (short-id, version, name)
    @type ai: C{list} of (C{None}, C{int}, C{str})

    @ivar gs: List of game scripts as (short-id, version, name)
    @type gs: C{list} of (C{None}, C{int}, C{str})
    """

    def __init__(self):
        self.md5sum = hashlib.md5()
        self.savegame_version = None
        self.map_size = (None, None)
        self.newgrf = []
        self.ai = []
        self.gs = []

    def read(self, file):
        """
        Read savegame meta data

        @param file: File to read
        @type file: File-like object

        @return: True on success.
        @rtype: C{bool}
        """

        try:
            reader = binreader.BinaryReader(file, self.md5sum)
            format = reader.read(4)
            self.savegame_version = reader.uint16(be=True)
            reader.uint16()

            decompressor = UNCOMPRESS.get(format)
            if decompressor is None:
                raise Exception("Unknown savegame compression")

            uncompressed = decompressor.open(reader)
            reader = binreader.BinaryReader(uncompressed)

            while True:
                tag = reader.read(4)
                if len(tag) == 0 or tag == b"\0\0\0\0":
                    break
                if len(tag) != 4:
                    raise Exception("Invalid savegame")

                type = reader.uint8()
                if (type & 0x0F) == 0x00:
                    size = type << 20 | reader.uint24(be=True)
                    self.read_item(tag, -1, reader.read(size))
                elif type == 1 or type == 2:
                    index = -1
                    while True:
                        size = reader.gamma()[0] - 1
                        if size < 0:
                            break
                        if type == 2:
                            index, index_size = reader.gamma()
                            size -= index_size
                        else:
                            index += 1
                        self.read_item(tag, index, reader.read(size))
        except Exception as e:
            print(e)
            return False
        finally:
            file.close()

        return True

    def read_item(self, tag, index, data):
        reader = binreader.BinaryReader(io.BytesIO(data))
        if tag == b"MAPS":
            size_x = reader.uint32(be=True)
            size_y = reader.uint32(be=True)
            self.map_size = (size_x, size_y)
        elif tag == b"NGRF":
            filename = reader.gamma_str().decode()
            grfid = reader.uint32(be=True)
            md5sum = reader.read(16).hex()
            if self.savegame_version >= 151:
                version = reader.uint32(be=True)
            else:
                version = None
            self.newgrf.append((grfid, md5sum, version, filename))
        elif tag == b"AIPL":
            name = reader.gamma_str().decode()
            settings = reader.gamma_str()
            if self.savegame_version >= 108:
                version = reader.uint32(be=True)
            else:
                version = None
            is_random = self.savegame_version >= 136 and reader.uint8() != 0
            if not is_random and len(name) > 0:
                self.ai.append((None, version, name))
        elif tag == b"GSDT":
            name = reader.gamma_str().decode()
            settings = reader.gamma_str()
            version = reader.uint32(be=True)
            is_random = reader.uint8() != 0
            if not is_random and len(name) > 0:
                self.gs.append((None, version, name))
