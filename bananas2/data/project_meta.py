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

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, UniqueConstraint, Index
from .tables import Base

class ProjectDescription(Base):
    """
    Description of project.

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar project: Project.id
    @type project: C{int}

    @ivar latest: Whether this is the latest version of this description.
    @type latest: C{bool}

    @ivar person: Unique Person.id, authoring this text.
    @type person: C{int}

    @ivar date: Post/edit date
    @type date: C{datetime}

    @ivar headers: Header lines, mostly for URLs and stuff.
    @type headers: C{list} of (C{str}, C{str})

    @ivar content: Project bla
    @type content: C{str}
    """

    __tablename__  = "project_descriptions"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    project        = Column(Integer,     ForeignKey("projects.id"), nullable=False, index=True)
    latest         = Column(Boolean,     nullable=False)
    person         = Column(Integer,     ForeignKey("persons.id"), nullable=False)
    date           = Column(DateTime,    nullable=False)
    headers        = Column(Text,        nullable=False) # JSON list of pairs
    content        = Column(Text,        nullable=False)
    __table_args__ = (Index("project_latest", "project", "latest"),)

class ProjectScreenshot(Base):
    """
    Screenshot for project.

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar project: Project.id
    @type project: C{int}

    @ivar person: Unique Person.id, authoring this text.
    @type person: C{int}

    @ivar date: Post date
    @type date: C{datetime}

    @ivar sort_index: Sorting index, None to hide/archive
    @type sort_index: C{str} or C{None}

    @ivar title: Name/Title
    @type title: C{str}

    @ivar description: Description
    @type description: C{str}

    @ivar file_id: Identifier in Blob storage
    @type file_id: C{int}
    """

    __tablename__  = "project_screenshots"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    project        = Column(Integer,     ForeignKey("projects.id"), nullable=False, index=True)
    person         = Column(Integer,     ForeignKey("persons.id"), nullable=False)
    date           = Column(DateTime,    nullable=False)
    sort_index     = Column(Integer,     nullable=True)
    title          = Column(String(150), nullable=False)
    description    = Column(Text,        nullable=False)
    file_id        = Column(Integer,     nullable=True)

class ProjectReview(Base):
    """
    User review for project.

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar project: Project.id
    @type project: C{int}

    @ivar person: Unique Person.id, authoring the first version of this text.
    @type person: C{int}

    @ivar latest: Whether this is the latest version of this review.
    @type latest: C{bool}

    @ivar edit_person: Last editing person, if not "person", i.e. a moderator.
    @type edit_person: C{int} or C{None}

    @ivar language: Language of review (isocode).
    @type language: C{str}

    @ivar date: Post/edit date
    @type date: C{datetime}

    @ivar rating: Review rating, if any
    @type rating: C{int} or C{None}

    @ivar title: Name/Title, if any content
    @type title: C{str} or C{None}

    @ivar content: User bla
    @type content: C{str} or C{None}
    """

    __tablename__  = "project_reviews"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    project        = Column(Integer,     ForeignKey("projects.id"), nullable=False, index=True)
    person         = Column(Integer,     ForeignKey("persons.id"), nullable=False)
    latest         = Column(Boolean,     nullable=False)
    edit_person    = Column(Integer,     ForeignKey("persons.id"), nullable=True)
    language       = Column(String(10),  nullable=False)
    date           = Column(DateTime,    nullable=False)
    rating         = Column(Integer,     nullable=True)
    title          = Column(String(150), nullable=True)
    content        = Column(Text,        nullable=True)
    __table_args__ = (Index("project_person", "project", "person"), Index("project_person_latest", "project", "person", "latest"))
