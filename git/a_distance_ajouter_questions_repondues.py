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
import json
import os
import re

import datetime
from datetime import datetime

import fuzzywuzzy
from fuzzywuzzy import fuzz

import git

import locale
locale.setlocale(locale.LC_ALL, ('fr_CA', 'UTF-8'))

LES_ETUDIANTS_PATH='les_etudiants.json'
REPONDUES_PATH='questions_repondues.json'

TAG_REPONSE = 'reponse'

FORMAT_DATE = '%A %d %B à %H:%M'

les_etudiants = {}

# par étudiant: un dict de questions répondues
questions_repondues = {}

def ajouter_questions_repondues():
    for numero in les_etudiants:

        depot = les_etudiants[numero]['depot']

        repo = git.Repo(depot)

        tags = repo.tags

        for tag in tags:

            nom_tag = tag.name

            ratio = fuzz.partial_ratio(TAG_REPONSE, nom_tag)


            if ratio > 65:

                commit = tag.commit

                if "prof" not in "branch --contains: " + repo.git.branch(contains=u""+nom_tag):
                    print u"pas sur branche prof: %s/%s" % (depot, nom_tag)
                    continue

                horodatage = commit.committed_date

                date = datetime.fromtimestamp(horodatage)

                if numero in questions_repondues:
                    if nom_tag in questions_repondues[numero]:
                        continue

                print u"nouvelle réponse: " + nom_tag

                nouvelle_reponse = {}
                nouvelle_reponse['horodatage'] = horodatage
                nouvelle_reponse['date'] = date.strftime(FORMAT_DATE).decode('utf-8')

                if numero not in questions_repondues:
                    questions_repondues[numero] = {}

                questions_repondues[numero][nom_tag] =  nouvelle_reponse



if __name__ == '__main__':
    with codecs.open(LES_ETUDIANTS_PATH, encoding='utf8') as fichier_les_etudiants:
        les_etudiants = json.loads(fichier_les_etudiants.read())

    with codecs.open(REPONDUES_PATH, encoding='utf8') as fichier_repondues:
        questions_repondues = json.loads(fichier_repondues.read())

    ajouter_questions_repondues()

    with codecs.open(REPONDUES_PATH, 'w', encoding='utf8') as fichier_repondues:
        fichier_repondues.write(json.dumps(questions_repondues, indent=4, ensure_ascii=False))
