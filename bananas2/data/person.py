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
class GlobalRole(enum.IntEnum):
    """
    Global role of a Person
    """
    ANONYMOUS  =  0  # Not logged in
    BANNED     =  1  # Banned user
    USER       = 10  # Regular user
    CURATOR    = 20  # Global curator
    MODERATOR  = 30  # Global moderator
    ADMIN      = 40  # Administrator

class Person(Base):
    """
    Person

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar username: Displayed nickname
    @type username: C{str} or C{None}

    @ivar tos_version: Version of Terms-Of-Service accepted.
    @type tos_version: C{str}

    @ivar role: Global permissions
    @type role: C{GlobalRole}
    """

    __tablename__  = "persons"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    username       = Column(String(150), nullable=False, unique=True)
    tos_version    = Column(String(30),  nullable=False)
    role           = Column(Integer,     nullable=False)

class Account(Base):
    """
    Accounts connected to persons.

    @ivar id: Unique id, never to be changed.
    @type id: C{int}

    @ivar domain: Account domain
    @type domain: C{str}

    @ivar login: Login name
    @type login: C{str}

    @ivar person: Person.id associated to this account.
    @type person: C{int}

    @ivar is_banned: When this account is allowed to login and identify as the linked person.
    @type is_banned: C{bool}
    """

    __tablename__  = "accounts"
    id             = Column(Integer,     primary_key=True, autoincrement=True)
    domain         = Column(String(150), nullable=False)
    login          = Column(String(150), nullable=False)
    person         = Column(Integer,     ForeignKey("persons.id"), nullable=False)
    is_banned      = Column(Boolean,     nullable=False)
    __table_args__ = (UniqueConstraint("domain", "login"),)
