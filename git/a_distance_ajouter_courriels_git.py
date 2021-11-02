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

import git

LES_ETUDIANTS_PATH='les_etudiants.json'

les_etudiants = {}

def ajouter_courriels_git():
    for numero in les_etudiants:
        depot = les_etudiants[numero]['depot']

        repo = git.Repo(depot)
        dernier_commit = repo.commit('master')

        courriel = dernier_commit.author.email

        if 'prabh' in courriel:
            courriel = courriel.replace('[','')
            courriel = courriel.replace(']','')

        courriel = courriel.lower()

        courriels = set(les_etudiants[numero]['courriels'])

        courriels.add(courriel)

        les_etudiants[numero]['courriels'] = list(courriels)




if __name__ == '__main__':
    with codecs.open(LES_ETUDIANTS_PATH, encoding='utf8') as fichier_les_etudiants:
        les_etudiants = json.loads(fichier_les_etudiants.read())

    ajouter_courriels_git()


    with codecs.open(LES_ETUDIANTS_PATH, 'w', encoding='utf8') as fichier_les_etudiants:
        fichier_les_etudiants.write(json.dumps(les_etudiants, indent=4, ensure_ascii=False))




