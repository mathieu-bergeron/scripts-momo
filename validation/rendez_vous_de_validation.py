#! /usr/bin/python
# vim: set fileencoding=utf8 :
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

import sys
import json
import codecs
import random
import datetime
from datetime import timedelta

if len(sys.argv) <= 3:
    print "usage %s in.json HEURE_DEBUT out.md" % sys.argv[0]
    exit(0)

INPUT_PATH = sys.argv[1]
HEURE_DEBUT = sys.argv[2]
OUTPUT_PATH = sys.argv[3]

ATELIER='TP'



annee = datetime.date.today().year
mois = datetime.date.today().month
jour = datetime.date.today().day
heure_debut = int(HEURE_DEBUT.split(':')[0])
minutes_debut = int(HEURE_DEBUT.split(':')[1])

heure_rendez_vous =  datetime.datetime(annee,mois,jour,heure_debut, minutes_debut)

TEMPS_RENDEZ_VOUS=timedelta(minutes=7)

def vers_liste_melangee(students_map):
    students = [students_map[x] for x in students_map]
    random.shuffle(students)
    return students

def vers_md(students):
    global heure_rendez_vous

    md = ""

    for student in students:
        md += "* "
        md += "*%s* " % heure_rendez_vous.strftime("%H:%M")
        md += student['name']
        md += " "
        md += student['surname']
        md += "\n"

        heure_rendez_vous += TEMPS_RENDEZ_VOUS

    return md

with codecs.open(INPUT_PATH, encoding='utf8') as input_file:

    json_in = input_file.read()

    students_map = json.loads(json_in)

    students = vers_liste_melangee(students_map)

    students_md = vers_md(students)

    with codecs.open(OUTPUT_PATH, 'w', encoding='utf8') as output_file:

        output_file.write(students_md)






