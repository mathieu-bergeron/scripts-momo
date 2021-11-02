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

# IMPORANT: input files must be UTF-8 
#           use e.g. vim with :set fileencoding=utf8 :w
ATELIER01_PATH='atelier01.csv'
TOUS_PATH='tous_les_etudiants.csv'

LES_ETUDIANTS_PATH='les_etudiants.json'


les_etudiants = {}
mes_etudiants = {}




def nettoyer_nom(nom_etudiant):
    nom_etudiant = nom_etudiant.replace('"','')
    nom_etudiant = nom_etudiant.replace(' ','_')
    nom_etudiant = nom_etudiant.replace(u'é','e')
    nom_etudiant = nom_etudiant.replace(u'è','e')
    nom_etudiant = nom_etudiant.replace(u'ê','e')
    nom_etudiant = nom_etudiant.replace(u'à','a')
    nom_etudiant = nom_etudiant.replace(u'â','a')
    nom_etudiant = nom_etudiant.replace(u'ç','c')

    return nom_etudiant

def lire_tous(fichier_tous, skip_first_line, separator):
    if skip_first_line:
        next(fichier_tous)

    for line in fichier_tous:
        fields = line.split(separator)

        nom = fields[0].lstrip()
        prenom = fields[1].lstrip()
        numero = fields[2].rstrip()

        courriel = fields[3].rstrip()
        courriel = courriel.lower()

        nom_etudiant = "%s %s" % (prenom, nom)
        nom_etudiant = nettoyer_nom(nom_etudiant)

        try:
            int(numero)
        except: 
            continue

        # registration_id is at least 9 digits long
        if len(numero) < 9:
            continue

        # remove non-unique prefix
        numero = numero[2:]

        if nom_etudiant in mes_etudiants:
            les_etudiants[numero] = {}
            les_etudiants[numero]['prenom'] = prenom
            les_etudiants[numero]['nom'] = nom
            les_etudiants[numero]['courriels'] = [courriel]
            les_etudiants[numero]['depot'] = mes_etudiants[nom_etudiant]['depot']


def lire_atelier01(fichier_atelier01, skip_first_line, separator):
    if skip_first_line:
        next(fichier_atelier01)

    for line in fichier_atelier01:
        fields = line.split(separator)
        repo_url = fields[9]

        student_name = fields[7]

        nom_etudiant = nettoyer_nom(student_name)

        mes_etudiants[nom_etudiant] = {}

        mes_etudiants[nom_etudiant]['depot'] = nom_etudiant





if __name__ == '__main__':
    with codecs.open(ATELIER01_PATH, encoding='utf8') as fichier_atelier01:
        lire_atelier01(fichier_atelier01, True, ',')

    with codecs.open(TOUS_PATH, encoding='utf8') as fichier_tous:
        lire_tous(fichier_tous, True, ';')

    with codecs.open(LES_ETUDIANTS_PATH, 'w', encoding='utf8') as fichier_les_etudiants:
        fichier_les_etudiants.write(json.dumps(les_etudiants, indent=4, ensure_ascii=False))



