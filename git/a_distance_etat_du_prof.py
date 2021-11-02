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

import git

import locale
locale.setlocale(locale.LC_ALL, ('fr_CA', 'UTF-8'))

PRIORITE_PATH='les_priorites.json'
LES_ETUDIANTS_PATH='les_etudiants.json'
EN_ATTENTE_PATH='questions_en_attente.json'
REPONDUES_PATH='questions_repondues.json'

PROCHAINE_SEANCE='prochaine_seance.md'

ETAT_DU_PROF='a_distance_etat_prof.md'

FORMAT_DATE = '%A %d %B à %H:%M'

les_etudiants = {}
liste_priorite = []
questions_en_attente = {}
questions_repondues = {}


def ecrire_questions_en_attente(fichier_etat):
    fichier_etat.write(u"\n\n")
    fichier_etat.write(u"## Liste des questions, par étudiant, par priorité")
    fichier_etat.write(u"\n\n")

    au_moins_une_question = False

    for numero in liste_priorite:
        if numero in questions_en_attente:

            fichier_etat.write(u"* %s" % numero )
            fichier_etat.write(u"\n")

            questions_brutes = questions_en_attente[numero]
            questions = []

            for nom_tag in questions_brutes.keys():

                au_moins_une_question = True

                horodatage = questions_brutes[nom_tag]['horodatage']
                date = datetime.fromtimestamp(horodatage)

                questions.append((nom_tag, date))

            questions.sort(key=lambda (nom,date): date)

            for (nom_tag, date) in questions:
                fichier_etat.write(u"\t1. %s: %s" % (nom_tag, date.strftime(FORMAT_DATE).decode('utf-8')) )
                fichier_etat.write(u"\n")

    if not au_moins_une_question:
        fichier_etat.write(u"\n\n")
        fichier_etat.write(u"* `liste vide`")
        fichier_etat.write(u"\n\n")

    fichier_etat.write(u"\n\n")

def ecrire_questions_repondues(fichier_etat):
    fichier_etat.write(u"\n\n")
    fichier_etat.write(u"## Liste des questions répondues")
    fichier_etat.write(u"\n\n")

    numeros = [int(numero) for numero in questions_repondues.keys()]
    numeros = sorted(numeros)

    for numero in numeros:
        fichier_etat.write(u"* %s" % numero )
        fichier_etat.write(u"\n")

        numero = str(numero)

        questions = questions_repondues[numero].keys()

        questions = sorted(questions, key=lambda nom_tag: int(questions_repondues[numero][nom_tag]['horodatage']))

        for nom_tag in questions:
            fichier_etat.write(u"\t1. %s: %s" % (nom_tag, questions_repondues[numero][nom_tag]['date']))
            fichier_etat.write(u"\n")



    fichier_etat.write(u"\n\n")
    fichier_etat.write(u"&nbsp;&nbsp;**SVP avertir le prof d'une erreur dans la liste**")
    fichier_etat.write(u"\n\n")


def ecrire_prochaine_seance(fichier_etat):
    with codecs.open(PROCHAINE_SEANCE, encoding='utf8') as fichier_prochaine_seance:
        fichier_etat.write(u"\n\n")
        fichier_etat.write(fichier_prochaine_seance.read())
        fichier_etat.write(u"\n\n")
        



def ecrire_etat_prof(fichier_etat):

    maintenant = datetime.now()

    fichier_etat.write(u"# %s " % (maintenant.strftime(FORMAT_DATE).decode('utf-8').capitalize()))
    fichier_etat.write(u"\n\n")
    fichier_etat.write(u"**Si ma question n'apparaît pas**:\n\n")
    fichier_etat.write(u"1. je pousse mon *prochain* tag `questionXX`\n")
    fichier_etat.write(u"1. j'attends 10 min\n")
    fichier_etat.write(u"1. je rafraîchis cette page\n")
    fichier_etat.write(u"\n\n")

    ecrire_questions_en_attente(fichier_etat)

    ecrire_prochaine_seance(fichier_etat)

    ecrire_questions_repondues(fichier_etat)


    fichier_etat.write(u"\n\n")
    fichier_etat.write(u"## Liste courante des priorités")
    fichier_etat.write(u"\n\n")

    for numero in liste_priorite:

        fichier_etat.write(u"1. %s" % numero )
        fichier_etat.write(u"\n")





if __name__ == '__main__':
    with codecs.open(LES_ETUDIANTS_PATH, encoding='utf8') as fichier_les_etudiants:
        les_etudiants = json.loads(fichier_les_etudiants.read())

    with codecs.open(REPONDUES_PATH, encoding='utf8') as fichier_repondues:
        questions_repondues = json.loads(fichier_repondues.read())

    with codecs.open(EN_ATTENTE_PATH, encoding='utf8') as fichier_en_attente:
        questions_en_attente = json.loads(fichier_en_attente.read())

    with codecs.open(PRIORITE_PATH, encoding='utf8') as fichier_priorites:
        liste_priorite = json.loads(fichier_priorites.read())

    with codecs.open(ETAT_DU_PROF, 'w', encoding='utf8') as fichier_etat:
        ecrire_etat_prof(fichier_etat)

