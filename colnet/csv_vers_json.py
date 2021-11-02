#! /usr/bin/python
# vim: set fileencoding=utf-8 :
#
# --
# Copyright (C) (2019) (Mathieu Bergeron) (mathieu.bergeron@cmontmorency.qc.ca)
# --
#
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
import json

if len(sys.argv) <= 2:
    print "usage %s in.csv separator out.json" % sys.argv[0]
    exit(0)

INPUT_PATH = sys.argv[1]
SEPARATOR = sys.argv[2]
POSITION_SURNAME = 0
POSITION_NAME = 1
POSITION_REGISTRATION_ID = 2
POSITION_PROGRAM = 3
POSITION_NOTE = 4
POSITION_PHONE = 5
OUTPUT_PATH = sys.argv[3]

def read_students(input_file):
    students={}

    for line in input_file:
        student={}

        fields = line.split(SEPARATOR)
        student['name'] = fields[POSITION_NAME].rstrip()
        student['surname'] = fields[POSITION_SURNAME].rstrip()
        student['registrationId'] = fields[POSITION_REGISTRATION_ID].rstrip()
        student['program'] = fields[POSITION_PROGRAM].rstrip()
        student['note'] = fields[POSITION_NOTE].rstrip()
        student['phone'] = fields[POSITION_PHONE].rstrip()

        _id = generate_id(student)

        students[_id] = student

    return students

ids = {}

def generate_id(student):
    global ids

    name = student['name']
    surname = student['surname']

    _id = name[0:2] + surname[0:3]

    _id = _id.lower()

    _id = remplacer_caracteres_speciaux(_id)

    _id = rendre_id_unique(ids, _id)

    ids[_id] = True

    return _id

def remplacer_caracteres_speciaux(chaine):
    chaine = chaine.replace(u'é','e')
    chaine = chaine.replace(u'è','e')
    chaine = chaine.replace(u'ê','e')
    chaine = chaine.replace(u'à','a')
    chaine = chaine.replace(u'â','a')
    chaine = chaine.replace(u'î','i')
    chaine = chaine.replace(u'ô','o')
    chaine = chaine.replace('.','')
    chaine = chaine.replace('-','')
    chaine = chaine.replace("'",'')
    chaine = chaine.replace(' ','')

    return chaine


def rendre_id_unique(ids, _id):
    while ids.has_key(_id):
        _id += random.choice("abcdefghijklmnopqrstuvwxyz")

    return _id

with codecs.open(INPUT_PATH, encoding='utf8') as input_file:

    students_map = read_students(input_file)

    with codecs.open(OUTPUT_PATH, 'w', encoding='utf8') as output_file:

        output_file.write(json.dumps(students_map, indent=4, ensure_ascii=False))
