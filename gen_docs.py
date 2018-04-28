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

from bananas2.data.tables import Base

print("@startuml")

for t in Base.metadata.tables.values():
    print("class {} {{".format(t.name))
    for col in t.columns:
        non_null = ""
        if col.nullable:
            non_null = " [0..1]"
        print("  {} : {}{}".format(col.name, col.type.__str__().partition("(")[0], non_null))
    print("}")
    refs = set(ref.column.table.name for ref in t.foreign_keys)
    for ref in refs:
        print("{} --> {}".format(t.name, ref))

print("@enduml")
