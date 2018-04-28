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

import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint, Index
from .tables import Base

@enum.unique
class VersionedFileType(enum.IntEnum):
    LICENSE      = 1 # License file
    README       = 2 # Readme file
    CHANGELOG    = 3 # Changelog file

class VersionedFile(Base):
    """
    Meta data textfiles which can be replaced without affecting the md5 of the content.
    These files are versioned to know which version was used in bundles at which point of time.

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar version: ProjectVersion.Id reference
    @type version: C{int}

    @ivar file_type: Type of file
    @type file_type: C{VersionedFileType}

    @ivar latest: Whether this is the latest version of this file.
    @type latest: C{bool}

    @ivar person: Person.id uploading this file.
    @type person: C{int}

    @ivar date: Upload date
    @type date: C{datetime}

    @ivar builtin_license: Name of non-custom license.
    @type builtin_license: C{str} or C{None}

    @ivar file_id: Identifier in Blob storage
    @type file_id: C{int} or C{None}

    TODO txt, md, pdf, ...?
    """

    __tablename__  = "versioned_files"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    version        = Column(Integer,     ForeignKey("project_versions.id"), nullable=False)
    file_type      = Column(Integer,     nullable=False)
    latest         = Column(Boolean,     nullable=False)
    person         = Column(Integer,     ForeignKey("persons.id"), nullable=False)
    date           = Column(DateTime,    nullable=False)
    builtin_license= Column(String(30),  nullable=True)
    file_id        = Column(Integer,     nullable=True)
    __table_args__ = (Index("version", "file_type"), Index("version", "file_type", "latest"))

class Bundle(Base):
    """
    Downloadable bundle including bundled meta files.

    | Content       | default                                                          | source   |
    | ------------- | ---------------------------------------------------------------- | -------- |
    | Base graphics | license, readme, changelog, .obg, 6x.grf                         | *        |
    | Base sounds   | license, readme, changelog, .obs, .cat                           | *        |
    | Base music    | license, readme, changelog, .obm, *.gm                           | *        |
    | NewGRF        | license, readme, changelog, .grf                                 | *        |
    | AI            | license, readme, changelog, info.nut, main.nut, *nut             | ---      |
    | GS            | license, readme, changelog, info.nut, main.nut, *nut, lang/*.txt | ---      |
    | AI/GS lib     | license, readme, changelog, library.nut, main.nut, *nut          | ---      |
    | Heightmap     | license, readme, changelog, .png, .png.id, .png.title            | ---      |
    | Scenario      | license, readme, changelog, .scn, .scn.id, .scn.title            | ---      |
    | NewGRF preset | .txt                                                             | ---      |
    | OpenTTD       | *                                                                | *        |

    @ivar version: ProjectVersion.Id reference
    @type version: C{int}

    @ivar bundle_type: "default", "source", "8bpp-1x", "linux-debian-jesse-amd64.deb", ...
    @type bundle_type: C{str}

    @ivar person: Person.id uploading this file.
    @type person: C{int}

    @ivar date: Upload date
    @type date: C{datetime}

    @ivar package_date: Date of lastest (re)packaging
    @type package_date: C{datetime}

    @ivar file_id: Identifier in Blob storage
    @type file_id: C{int}

    @ivar checksum_md5: Checksum md5
    @type checksum_md5: C{str}

    @ivar checksum_sha1: Checksum sha1
    @type checksum_sha1: C{str}

    @ivar checksum_sha256: Checksum sha256
    @type checksum_sha256: C{str}

    TODO cached filename, cached filesize, cached visibility, mirror status, download count
    """

    __tablename__  = "bundles"
    version        = Column(Integer,     ForeignKey("project_versions.id"), primary_key=True, index=True)
    bundle_type    = Column(String(50),  primary_key=True)
    person         = Column(Integer,     ForeignKey("persons.id"), nullable=False)
    date           = Column(DateTime,    nullable=False)
    package_date   = Column(DateTime,    nullable=False)
    file_id        = Column(Integer,     nullable=False)
    checksum_md5   = Column(String(32),  nullable=False)
    checksum_sha1  = Column(String(40),  nullable=False)
    checksum_sha256= Column(String(64),  nullable=False)

    BUNDLE_SOURCE     = "source"    # Source package for open-source content
    BUNDLE_DEFAULT    = "default"   # Binary package, if not further distinguished (base sounds, base music, AI, AI lib, GS, GS lib, heightmap, scenario, newgrf preset)
    BUNDLE_32BPP      = "32bpp"     # Full NewGRF package (base graphics, NewGRF)
    BUNDLE_32BPP_1X   = "32bpp-1x"  # NewGRF package, stripped from extra zoom
    BUNDLE_8BPP       = "8bpp"      # NewGRF package, stripped from 32bpp
    BUNDLE_8BPP_1x    = "8bpp-1x"   # NewGRF package, stripped from extra zoom and 32bpp
