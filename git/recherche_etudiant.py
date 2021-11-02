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
import sys

import fuzzywuzzy
from fuzzywuzzy import fuzz

import locale
locale.setlocale(locale.LC_ALL, ('fr_CA', 'UTF-8'))

LES_ETUDIANTS_PATH='les_etudiants.json'

les_etudiants = {}
etudiants_trouves = {}


def chercher_etudiant(critere_recherche):

    critere_recherche = critere_recherche.lower()

    for numero in les_etudiants:

        etudiant = les_etudiants[numero]

        ratio = fuzz.partial_ratio(critere_recherche, numero)

        if ratio > 80:
            etudiants_trouves[numero] = etudiant
            continue

        ratio = fuzz.partial_ratio(critere_recherche, etudiant['prenom'].lower())

        if ratio > 80:
            etudiants_trouves[numero] = etudiant
            continue

        ratio = fuzz.partial_ratio(critere_recherche, etudiant['nom'].lower())

        if ratio > 80:
            etudiants_trouves[numero] = etudiant
            continue

def afficher_etudiants(dict_etudiants):

    for numero in dict_etudiants:

        etudiant = dict_etudiants[numero]

        print ""

        print "%s %s %s %s" % (numero, etudiant['prenom'], etudiant['nom'], " ".join([str(courriel) for courriel in etudiant['courriels']]))



if __name__ == '__main__':

    critere_recherche = ""

    if len(sys.argv) == 2:
        critere_recherche = sys.argv[1]
    else:
        print "usage: python %s CRITERE_RECHERCHE" % sys.argv[0]

    with codecs.open(LES_ETUDIANTS_PATH, encoding='utf8') as fichier_les_etudiants:
        les_etudiants = json.loads(fichier_les_etudiants.read())

    chercher_etudiant(critere_recherche)

    print ""

    afficher_etudiants(etudiants_trouves)

    print ""


