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

import enum
import hashlib
from io import BytesIO
from bananas2.data import language
from . import binreader

@enum.unique
class Feature(enum.IntEnum):
    """
    NewGRF features
    """
    TRAINS          = 0x00,
    ROAD_VEHICLES   = 0x01,
    SHIPS           = 0x02,
    AIRCRAFT        = 0x03,
    STATIONS        = 0x04,
    CANALS          = 0x05,
    BRIDGES         = 0x06,
    HOUSES          = 0x07,
    INDUSTRY_TILES  = 0x09,
    INDUSTRIES      = 0x0A,
    CARGOS          = 0x0B,
    SOUND_EFFECTS   = 0x0C,
    AIRPORTS        = 0x0D,
    SIGNALS         = 0x0E,
    OBJECTS         = 0x0F,
    RAILTYPES       = 0x10,
    AIRPORT_TILES   = 0x11,
    TOWNNAMES       = 0x101,

class NewGRF:
    """
    NewGRF meta data.

    @ivar grf_id: Grf ID
    @type grf_id: C{int} or C{None}

    @ivar md5sum: md5 checksum
    @type md5sum: C{hash}

    @ivar grf_version: NewGRF spec version
    @type grf_version: C{int} or C{None}

    @ivar name: Name of NewGRF
    @type name: C{dict} of C{str}

    @ivar version: Version of NewGRF
    @type version: C{int} or C{None}

    @ivar min_compatible_version: Minimum compatible version when loading savegames with older NewGRF
    @type min_compatible_version: C{int} or C{None}

    @ivar description: Description of NewGRF
    @type description: C{dict} of C{str}

    @ivar url: URL of NewGRF
    @type url: C{dict} of C{str}

    @ivar container_version: GRF container version: 1, 2
    @ivar container_version: C{int}

    @ivar has_32bpp: Whether 32bpp sprites are present.
    @type has_32bpp: C{bool}

    @ivar max_zoomin: Maximum zoom-in level: 1, 2, 4
    @type max_zoomin: C{int}

    @ivar features: Used NewGRF features
    @type features: C{set} of C{Feature}
    """

    def __init__(self):
        self.grf_id = None
        self.md5sum = hashlib.md5()
        self.grf_version = None
        self.name = dict()
        self.version = None
        self.min_compatible_version = None
        self.description = dict()
        self.url = dict()
        self.container_version = None
        self.has_32bpp = False
        self.max_zoomin = 1
        self.features = set()

    def read(self, file):
        """
        Read NewGRF meta data

        @param file: File to read
        @type file: File-like object

        @return: True on success.
        @rtype: C{bool}
        """

        reader = binreader.BinaryReader(file, self.md5sum)

        try:
            size = reader.uint16()
            if size == 0:
                if reader.read(8) == b'GRF\x82\r\n\x1A\n':
                    self.container_version = 2
                    reader.uint32()
                    if reader.uint8() != 0:
                        raise Exception("Unknown container 2 compression")
                    size = reader.uint32()
                else:
                    raise Exception("neither container 1 nor 2")
            else:
                self.container_version = 1

            skip_sprites = 0
            first_pseudo = True
            while size != 0:
                info = reader.uint8()
                if info == 0xFF:
                    if skip_sprites > 0:
                        reader.skip(size)
                        skip_sprites -= 1
                    else:
                        pseudo = reader.read(size)
                        if not first_pseudo:
                            skip_sprites = self.read_pseudo(pseudo)
                else:
                    if skip_sprites > 0:
                        skip_sprites -= 1

                    if info == 0xFD and self.container_version == 2:
                        reader.skip(size)
                    elif self.container_version == 1 and size >= 8:
                        reader.skip(7)
                        size -= 8
                        if (info & 0x02) != 0:
                            reader.skip(size)
                        else:
                            while size > 0:
                                i = reader.uint8()
                                if i < 0x80:
                                    if i == 0:
                                        i = 0x80
                                    reader.skip(i)
                                else:
                                    i = 32 - (i >> 3)
                                    reader.skip(1)
                                if i > size:
                                    raise Exception("Failed sprite decoding")
                                size -= i
                    else:
                        raise Exception("Unknown info byte")

                first_pseudo = False
                if self.container_version == 2:
                    size = reader.uint32()
                else:
                    size = reader.uint16()

            if self.container_version == 1:
                reader.uint32()

            reader.detach_hash()

            if self.container_version == 2:
                id = reader.uint32()
                while id != 0:
                    size = reader.uint32()
                    info = reader.uint8()
                    zoom = reader.uint8()

                    if info != 0xFF:
                        if (info & 0x03) != 0:
                            self.has_32bpp = True
                        if zoom == 0x01:
                            self.max_zoomin = 4;
                        elif zoom == 0x02 and self.max_zoomin < 2:
                            self.max_zoomin = 2

                    reader.skip(size - 2)
                    id = reader.uint32()

        except Exception as e:
            print(e)
            return False
        finally:
            file.close()

        if self.grf_id is None:
            # If there was no Action 8 (e.g. BaseSet), then clear any bogus features that were added by recolour sprites
            self.features = set()

        return True

    def read_pseudo(self, pseudo):
        """
        Read and parse pseudo sprite

        @param pseudo: Pseudo sprite
        @type pseudo: C{bytes}

        @return: Number of sprites to skip.
        @rtype: C{int}
        """

        reader = binreader.BinaryReader(BytesIO(pseudo))

        action = reader.uint8()
        if action == 0x00 or action == 0x03 or action == 0x04:
            feat = reader.uint8()
            if feat in Feature._value2member_map_:
                self.features.add(Feature(feat))
        elif action == 0x01:
            reader.uint8()
            num_sets = reader.uint8()
            if num_sets == 0:
                reader.uint_ext()
                num_sets = reader.uint_ext()
            num_ent = reader.uint_ext()
            return num_sets * num_ent
        elif action == 0x05:
            reader.uint8()
            return reader.uint_ext()
        elif action == 0x08:
            self.grf_version = reader.uint8()
            self.grf_id = reader.uint32()
            self.name[None] = self.decodestr(reader.str())
            self.description[None] = self.decodestr(reader.str())
        elif action == 0x0A:
            return reader.uint8() * reader.uint8()
        elif action == 0x0F:
            self.features.add(Feature.TOWNNAMES)
        elif action == 0x11:
            self.features.add(Feature.SOUND_EFFECTS)
            return reader.uint16()
        elif action == 0x12:
            num_defs = reader.uint8()
            num_chars = 0
            while num_defs > 0:
                reader.uint8()
                num_chars += reader.uint8()
                reader.uint16()
                num_defs -= 1
            return num_chars
        elif action == 0x14:
            self.read_a14(reader, bytearray())

        return 0

    def read_a14(self, reader, path):
        """
        Read Action 14

        @param reader: Pseudo sprite reader
        @type reader: C{BinaryReader}

        @param path: Action 14 path
        @type path: C{list} of C{bytes}
        """

        while True:
            type = reader.uint8()
            if type == 0:
                return True

            subpath = path + reader.read(4)
            if type == ord("C"):
                if not self.read_a14(reader, subpath):
                    return False
            elif type == ord("B"):
                size = reader.uint16()
                data = binreader.BinaryReader(BytesIO(reader.read(size)))

                if subpath == b"INFOVRSN" and size > 4:
                    self.version = data.uint32()
                elif subpath == b"INFOMINV" and size > 4:
                    self.min_compatible_version = data.uint32()

            elif type == ord("T"):
                grflangid = reader.uint8()
                data = self.decodestr(reader.str())

                lang = language.GRFLANGID.get(grflangid)
                isocode = None
                if lang:
                    isocode = lang.isocode

                if grflangid == 0x7F or isocode:
                    if subpath == b"INFONAME":
                        self.name[isocode] = data
                    elif subpath == b"INFODESC":
                        self.description[isocode] = data
                    elif subpath == b"INFOURL_":
                        self.url[isocode] = data

            else:
                return False

    @staticmethod
    def getutf8(b, pos):
        if pos + 1 <= len(b) and (b[pos] & 0x80) == 0:
            return (1, b[pos])
        elif pos + 2 <= len(b) and (b[pos] & 0xE0) == 0xC0 and (b[pos + 1] & 0xC0) == 0x80:
            return (2, (b[pos] & 0x1F) << 6 | (b[pos + 1] & 0x3F))
        elif pos + 3 <= len(b) and (b[pos] & 0xF0) == 0xE0 and (b[pos + 1] & 0xC0) == 0x80 and (b[pos + 2] & 0xC0) == 0x80:
            return (3, (b[pos] & 0x0F) << 12 | (b[pos + 1] & 0x3F) << 6 | (b[pos + 2] & 0x3F))
        elif pos + 4 <= len(b) and (b[pos] & 0xF8) == 0xF0 and (b[pos + 1] & 0xC0) == 0x80 and (b[pos + 2] & 0xC0) == 0x80 and (b[pos + 3] & 0xC0) == 0x80:
            return (4, (b[pos] & 0x07) << 18 | (b[pos + 1] & 0x3F) << 12 | (b[pos + 2] & 0x3F) << 6 | (b[pos + 3] & 0x3F))
        else:
            return (0, None)

    ctrl_codes = {
        0x01: (1, " "), # SETX
        0x0E: (0, "") , # SMALLFONT
        0x0F: (0, ""),  # BIGFONT
        0x1F: (2, " "), # SETXY
        0x7B: (0, " "),
        0x7C: (0, " "),
        0x7D: (0, " "),
        0x7E: (0, " "),
        0x7F: (0, " "),
        0x80: (0, " "),
        0x81: (2, " "),
        0x82: (0, " "),
        0x83: (0, " "),
        0x84: (0, " "),
        0x85: (0, " "),
        0x86: (0, " "),
        0x87: (0, " "),
        0x88: (0, ""),  # BLUE
        0x89: (0, ""),  # SILVER
        0x8A: (0, ""),  # GOLD
        0x8B: (0, ""),  # RED
        0x8C: (0, ""),  # PURPLE
        0x8D: (0, ""),  # LTBROWN
        0x8E: (0, ""),  # ORANGE
        0x8F: (0, ""),  # GREEN
        0x90: (0, ""),  # YELLOW
        0x91: (0, ""),  # DKGREEN
        0x92: (0, ""),  # CREAM
        0x93: (0, ""),  # BROWN
        0x94: (0, ""),  # WHITE
        0x95: (0, ""),  # LTBLUE
        0x96: (0, ""),  # GRAY
        0x97: (0, ""),  # DKBLUE
        0x98: (0, ""),  # BLACK
        0x99: (0, ""),  # BLUE
        0x9E: (0, "\u20AC"),
        0x9F: (0, "\u0178"),
        0xA0: (0, "\u25B2"),
        0xAA: (0, "\u25BC"),
        0xAC: (0, "\u2713"),
        0xAD: (0, "\u274C"),
        0xAF: (0, "\u25B6"),
        0xB4: (0, ""), # train
        0xB5: (0, ""), # lorry
        0xB6: (0, ""), # bus
        0xB7: (0, ""), # plane
        0xB8: (0, ""), # ship
        0xB9: (0, "\u208B\u2081"),
        0xBC: (0, "\u2191"),
        0xBD: (0, "\u2193"),
    }

    ext_ctrl_codes = {
        0x01: (0, " "),
        0x03: (2, ""),
        0x04: (1, ""),
        0x06: (0, " "),
        0x07: (0, " "),
        0x08: (0, " "),
        0x0B: (0, " "),
        0x0C: (0, " "),
        0x0D: (0, " "),
        0x0E: (1, ""),
        0x0F: (1, ""),
        0x10: (1, ""),
        0x11: (1, ""),
        0x12: (0, ""),
        0x13: (1, ""),
        0x14: (0, ""),
        0x15: (1, ""),
        0x16: (0, " "),
        0x17: (0, " "),
        0x18: (0, " "),
        0x19: (0, " "),
        0x1A: (0, " "),
        0x1B: (0, " "),
        0x1C: (0, " "),
        0x1D: (0, " "),
        0x1E: (0, " "),
    }

    @staticmethod
    def decodestr(b):
        pos = 0
        is_unicode = NewGRF.getutf8(b, pos) == (2, 0x00DE)
        if is_unicode:
            pos += 2
        result = ""
        while pos < len(b):
            if is_unicode:
                size, c = NewGRF.getutf8(b, pos)
                if size == 0:
                    c = 0xE000 + b[pos]
                    pos += 1
                else:
                    pos += size
            else:
                c = b[pos]
                pos += 1
                if c in NewGRF.ctrl_codes:
                    c = 0xE000 + c

            if c == 13:
                result += "\n"
            elif c == 0xE09A:
                c = b[pos]
                pos += 1
                size, c = NewGRF.ext_ctrl_codes.get(c, (0, ""))
                pos += size
                result += c
            elif c >= 0xE000 and c <= 0xE0FF:
                size, c = NewGRF.ctrl_codes.get(c - 0xE000, (0, ""))
                pos += size
                result += c
            elif c >= 32:
                result += chr(c)

        return result
