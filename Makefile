# This file is part of BaNaNaS2, an Add-on Content Management System for OpenTTD.
# Copyright (C) 2018  Christoph Elsenhans
#
# BaNaNaS2 is free software; you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 2.
#
# BaNaNaS2 is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU General Public License for more details. You should have received a copy of the
# GNU General Public License along with BaNaNaS2. If not, see <http://www.gnu.org/licenses/>.

.PHONY: all docs html_docs

P3 = python3
PU = env -u DISPLAY plantuml

all: html_docs

# The results of "docs" unfortunately result in modifies in the checkout, so do not do it by default
docs: docs/tables.png

docs/tables.pu: bananas2/data/*.py gen_docs.py
	$(P3) gen_docs.py > $@

%.png: %.pu
	$(PU) $^

FILES_MD = $(wildcard docs/*.md)
FILES_HTML = $(FILES_MD:%.md=%.html)

html_docs: $(FILES_HTML)

%.html: %.md
	$(P3) -m markdown -x gfm $^ > $@
