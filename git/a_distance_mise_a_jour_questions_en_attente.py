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
EN_ATTENTE_PATH='questions_en_attente.json'
REPONDUES_PATH='questions_repondues.json'

TAG_QUESTION = 'question'

FORMAT_DATE = '%A %d %B à %H:%M'

les_etudiants = {}

# par étudiant: un dict de questions en attente
questions_en_attente = {}

# par étudiant: un dict de questions répondues
questions_repondues = {}

def charger_questions_en_attente():
    for numero in les_etudiants:

        depot = les_etudiants[numero]['depot']

        repo = git.Repo(depot)
        tags = repo.tags

        for tag in tags:

            nom_tag = tag.name

            ratio = fuzz.partial_ratio(TAG_QUESTION, nom_tag)

            if ratio > 65:

                commit = tag.commit
                horodatage = commit.committed_date

                date = datetime.fromtimestamp(horodatage)

                if numero in questions_repondues:
                    if nom_tag in questions_repondues[numero]:
                        continue


                print u"nouvelle question: %s/%s" % (depot, nom_tag)

                nouvelle_question = {}
                nouvelle_question['horodatage'] = horodatage
                nouvelle_question['date'] = date.strftime(FORMAT_DATE).decode('utf-8')

                if numero not in questions_en_attente:
                    questions_en_attente[numero] = {}

                questions_en_attente[numero][nom_tag] =  nouvelle_question



if __name__ == '__main__':
    with codecs.open(LES_ETUDIANTS_PATH, encoding='utf8') as fichier_les_etudiants:
        les_etudiants = json.loads(fichier_les_etudiants.read())

    with codecs.open(REPONDUES_PATH, encoding='utf8') as fichier_repondues:
        questions_repondues = json.loads(fichier_repondues.read())

    charger_questions_en_attente()

    with codecs.open(EN_ATTENTE_PATH, 'w', encoding='utf8') as fichier_en_attente:
        fichier_en_attente.write(json.dumps(questions_en_attente, indent=4, ensure_ascii=False))
