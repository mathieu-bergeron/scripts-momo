#! /usr/bin/python
# vim: set fileencoding=utf-8 :
#
# --
# git_clone.py  clone git repos from a .csv file
# --
# Copyright (C) (2018) (Mathieu Bergeron) (mathieu.bergeron@cmontmorency.qc.ca)
# --
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU AFFERO General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# or see http://www.gnu.org/licenses/agpl.txt.
# --

import codecs
import os
import sys
import re

# IMPORANT: input files must be UTF-8 
#           use e.g. vim with :set fileencoding=utf8 :w
INPUT_PATH='atelier02.csv'

SKIP_FIRST_LINE=True

SEPARATOR=','

NAME=sys.argv[1]

NAME_RE = re.compile(NAME, re.IGNORECASE)


with codecs.open(INPUT_PATH, encoding='utf8') as input_file:
    if SKIP_FIRST_LINE:
        next(input_file)

    for line in input_file:
        match = NAME_RE.search(line)

        if match is not None:
            fields = line.split(SEPARATOR)
            student_name = fields[7]
            student_id = fields[8]

            print student_name, student_id

