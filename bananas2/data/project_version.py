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
class VersionVisibility(enum.IntEnum):
    PENDING      =  1 # Version is being uploaded/prepared
    HIDDEN       =  2 # Version is hidden from new users
    EXPERIMENTAL = 10 # Experimental version for brave souls
    ARCHIVED     = 20 # Archived versions for old souls
    STABLE       = 30 # Version offered to normal users

class ProjectVersion(Base):
    """
    Version of a project.

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar project: Project.Id reference
    @type project: C{int}

    @ivar latest: Whether this is the latest version of this project. (used for public license, readme, changelog)
    @type latest: C{bool}

    @ivar name: Name of the version
    @type name: C{str}

    @ivar version_id: NewGRF version, Script version, Scenario version, ... not all project types have this
    @type version_id: C{int} or C{None}

    @ivar md5sum: Checksum identifying this version, if this content is identified using checksums.
    @type md5sum: C{str} or C{None}

    @ivar date: Upload date
    @type date: C{datetime}

    @ivar visibility: User-visibility of this version.
    @type visibility: C{VersionVisibility}
    """

    __tablename__  = "project_versions"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    project        = Column(Integer,     ForeignKey("projects.id"), nullable=False, index=True)
    latest         = Column(Boolean,     nullable=False)
    name           = Column(String(150), nullable=False)
    version_id     = Column(Integer,     nullable=True)
    md5sum         = Column(String(32),  nullable=True)
    date           = Column(DateTime,    nullable=False)
    visibility     = Column(Integer,     nullable=False)
    __table_args__ = (UniqueConstraint("project", "name"), UniqueConstraint("project", "version_id"), UniqueConstraint("project", "md5sum"))

class FeatureDependency(Base):
    """
    Content requires OpenTTD with specific feature set.

    Example: "OpenTTD.official" >= 0x18080000

    @ivar version: ProjectVersion.Id reference
    @type version: C{int}

    @ivar req_feature: Feature name
    @type req_feature: C{str}

    @ivar req_version_min: Minimum Version of feature
    @type req_version_min: C{int} or C{None}

    @ivar req_version_max: Maximum Version of feature
    @type req_version_max: C{int} or C{None}
    """

    __tablename__  = "feature_dependencies"
    version        = Column(Integer,     ForeignKey("project_versions.id"), primary_key=True, index=True)
    req_feature    = Column(String(50),  primary_key=True)
    req_version_min= Column(Integer,     nullable=True)
    req_version_max= Column(Integer,     nullable=True)

    FEATURE_OPENTTD_OFFICIAL = "OpenTTD.official"

class ContentDependency(Base):
    """
    Content requireing other content.

    @ivar version: ProjectVersion.Id reference
    @type version: C{int}

    @ivar req_project: Prerequisite Project.Id reference
    @type req_project: C{int}

    @ivar req_version: Prerequisite ProjectVersion.Id reference, if a single specific version is required.
    @type req_version: C{int} or C{None}

    @ivar req_version_min: Prerequisite ProjectVersion.version_id, minimum version, if a range of versions can be used.
    @type req_version_min: C{int} or C{None}

    @ivar req_version_max: Prerequisite ProjectVersion.version_id, maximum version, if a range of versions can be used.
    @type req_version_max: C{int} or C{None}
    """

    __tablename__  = "content_dependencies"
    version        = Column(Integer,     ForeignKey("project_versions.id"), primary_key=True, index=True)
    req_project    = Column(Integer,     ForeignKey("projects.id"), primary_key=True)
    req_version    = Column(Integer,     ForeignKey("project_versions.id"), nullable=True)
    req_version_min= Column(Integer,     nullable=True)
    req_version_max= Column(Integer,     nullable=True)
