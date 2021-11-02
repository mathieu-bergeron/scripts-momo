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
#INPUT_PATH='4205B5MO-000002.csv'
#OUTPUT_PATH='noms2.html' 

if len(sys.argv) <= 2:
    print "usage %s in.csv {out.html|out.txt}"
    exit(0)

INPUT_PATH=sys.argv[1]
OUTPUT_PATH=sys.argv[2]

SKIP_FIRST_LINE=True

SEPARATOR=';'


def process(INPUT_PATH, OUTPUT_PATH):
    with codecs.open(OUTPUT_PATH, 'w', encoding='utf8') as output_file:
        if 'html' in OUTPUT_PATH:
            output_file.write(" <meta charset='UTF-8'>\n")
            output_file.write("<table>\n")

        with codecs.open(INPUT_PATH, encoding='utf8') as input_file:
            if SKIP_FIRST_LINE:
                next(input_file)

            for line in input_file:
                fields = line.split(SEPARATOR)
                name = fields[1]
                surname = fields[0]

                if 'html' in OUTPUT_PATH:
                    output_file.write( "<tr>\n")
                    output_file.write( "<td>")

                output_file.write( name+" "+surname)

                if 'html' not in OUTPUT_PATH:
                    output_file.write("\n")

                if 'html' in OUTPUT_PATH:
                    output_file.write( "</td>\n")
                    output_file.write( "<tr>\n")

        if 'html' in OUTPUT_PATH:
            output_file.write( "</table>\n")


process(INPUT_PATH, OUTPUT_PATH)

INPUT_PATH='4205B5MO-000001.csv'
OUTPUT_PATH='noms1.html'

process(INPUT_PATH, OUTPUT_PATH)
