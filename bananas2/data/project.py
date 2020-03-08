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
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, UniqueConstraint
from .tables import Base

@enum.unique
class ProjectType(enum.IntEnum):
    """
    Type of a project
    """
    BASE_GRAPHICS =  1
    BASE_SOUNDS   =  2
    BASE_MUSIC    =  3
    NEWGRF        = 10
    AI            = 20
    AI_LIB        = 21
    GS            = 22
    GS_LIB        = 23
    HEIGHTMAP     = 30
    SCENARIO      = 31
    NEWGRF_PRESET = 40
    OPENTTD       = 50

@enum.unique
class ProjectRole(enum.IntEnum):
    """
    Role of a person in a project.
    The integer values are kept distinct from GlobalRole
    """
    OWNER     = 100
    EDITOR    = 110


class ProjectOptions(enum.IntEnum): # IntFlag in Python 3.6
    """
    Toggle options for projects.
    """
    CURATOR_EDIT_LABELS      = 0x0001
    CURATOR_EDIT_DESCRIPTION = 0x0002
    CURATOR_EDIT_SCREENSHOTS = 0x0004
    CURATOR_EDIT_FEATURE_DEPS= 0x0008
    USER_ALLOW_REVIEW        = 0x0100
    USER_ALLOW_RATING        = 0x0200

class Project(Base):
    """
    Content project.

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar type: Project type
    @type type: Project.TYPE_xxx

    @ivar content_id: NewGRF Id, Script Short Id, ... not all project types have this
    @type content_id: C{str} or C{None}

    @ivar name: Name of the project
    @type name: C{str}

    @ivar is_banned: Project is blocked from viewing and downloading.
    @type is_banned: C{bool}

    @ivar options: Toggle options for projects
    @type options: C{ProjectOptions}
    """

    __tablename__  = "projects"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    type           = Column(Integer,     nullable=False, index=True)
    content_id     = Column(String(8),   nullable=True)
    name           = Column(String(150), nullable=False)
    is_banned      = Column(Boolean,     nullable=False)
    options        = Column(Integer,     nullable=False)
    __table_args__ = (UniqueConstraint("type", "content_id"), UniqueConstraint("type", "name"))

class ProjectMember(Base):
    """
    Relation: Project-Person

    @ivar project: Unique Project.id
    @type project: C{int}

    @ivar person: Unique Person.id
    @type person: C{int}

    @ivar role: Membership type
    @type role: C{ProjectRole}
    """

    __tablename__  = "project_members"
    project        = Column(Integer,     ForeignKey("projects.id"), primary_key=True)
    person         = Column(Integer,     ForeignKey("persons.id"), primary_key=True)
    role           = Column(Integer,     nullable=False)

class ProjectLabel(Base):
    """
    Relation: Project-Label

    @ivar project: Unique Project.id
    @type project: C{int}

    @ivar label: Unique Label.id
    @type label: C{int}
    """

    __tablename__  = "project_labels"
    project        = Column(Integer,     ForeignKey("projects.id"), primary_key=True)
    label          = Column(Integer,     ForeignKey("labels.id"), primary_key=True)
