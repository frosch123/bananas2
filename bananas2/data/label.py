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

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from .tables import Base

class LabelCategory(Base):
    """
    Category for labels

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar name: Name of the label (level 2)
    @type name: C{str}

    @ivar description: Description
    @type description: C{str}

    @ivar project_types: List of project types which may use labels from this category.
    @type project_types: C{set} of C{int}
    """

    __tablename__  = "label_categories"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    name           = Column(String(150), nullable=False) # not unique to allow same category names with different labels for different project types
    description    = Column(String(300), nullable=False) # not unique to allow same category names with different labels for different project types
    project_type   = Column(String(150), nullable=False) # JSON list of project type

class Label(Base):
    """
    Label for categorisation.

    Labels are organised as a tree with two levels.
    * Label category
    * Label

    Examples:
    | Label category   | Labels...                                     |
    | ---------------- | --------------------------------------------- |
    | Content scale    | Full-featured set, Single item, ...           |
    | Geography        | Europe, South America, Spain, ...             |
    | NewGRF features  | Trains, Stations, Industries, Townnames, ...  |
    | Graphics style   | 32bpp, 4x, ...                                |
    | Map size         | 1k x 1k, 256 x 256, ...                       |
    | Play style       | Realism, Transport madness, Competitive, ...  |

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar category: Label category
    @type category: C{int}

    @ivar name: Name of the label
    @type name: C{str}

    @ivar description: Description
    @type description: C{str}
    """

    __tablename__  = "labels"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    category       = Column(Integer,     ForeignKey("label_categories.id"), nullable=False)
    name           = Column(String(150), nullable=False)
    description    = Column(String(300), nullable=False)
    __table_args__ = (UniqueConstraint("category", "name"),)
