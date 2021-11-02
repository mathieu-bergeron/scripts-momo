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
import random


LES_ETUDIANTS_PATH='les_etudiants.json'
PRIORITE_PATH='les_priorites.json'
EN_ATTENTE_PATH='questions_en_attente.json'
REPONDUES_PATH='questions_repondues.json'

les_etudiants = {}
liste_priorite = []

# par étudiant, la liste de questions
questions_en_attente = {}

# par étudiant, les questions déjà répondues
questions_repondues = {}

def creer_liste_priorite():
    global liste_priorite

    liste_priorite = les_etudiants.keys()
    random.shuffle(liste_priorite)


if __name__ == '__main__':
    with codecs.open(LES_ETUDIANTS_PATH, encoding='utf8') as fichier_les_etudiants:
        les_etudiants = json.loads(fichier_les_etudiants.read())

    creer_liste_priorite()

    with codecs.open(PRIORITE_PATH, 'w', encoding='utf8') as fichier_priorite:
        fichier_priorite.write(json.dumps(liste_priorite, indent=4, ensure_ascii=False))
