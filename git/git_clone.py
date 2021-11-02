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

from __future__ import print_function
import codecs
import os

# IMPORANT: input files must be UTF-8 
#           use e.g. vim with :set fileencoding=utf8 :w
INPUT_PATH='urls_git.csv'

SKIP_FIRST_LINE=True

SEPARATOR=','

GIT_CLONE='git clone '

USAGER_GITHUB='mathieu-bergeron'
MDP_GITHUB='Idgotoc1!'


def nettoyer_nom(nom_etudiant):


    nom_etudiant = nom_etudiant.replace(u'"',u'')
    nom_etudiant = nom_etudiant.replace(u"'",u'_')
    nom_etudiant = nom_etudiant.replace(u' ',u'_')
    nom_etudiant = nom_etudiant.replace(u'é','e')
    nom_etudiant = nom_etudiant.replace(u'è','e')
    nom_etudiant = nom_etudiant.replace(u'ê','e')
    nom_etudiant = nom_etudiant.replace(u'à','a')
    nom_etudiant = nom_etudiant.replace(u'â','a')
    nom_etudiant = nom_etudiant.replace(u'ä','a')
    nom_etudiant = nom_etudiant.replace(u'ë','e')
    nom_etudiant = nom_etudiant.replace(u'ï','i')
    nom_etudiant = nom_etudiant.replace(u'ç','c')

    return nom_etudiant

def inserer_mon_usager(url_depot):

    url_depot = url_depot.replace(u'github.com', u"%s:%s@github.com" % (USAGER_GITHUB, MDP_GITHUB))


    return url_depot


def prenom_en_premier(nom_etudiant):

    elements = nom_etudiant.split(' ')

    dernier_element = elements[-1]

    premiers_elements = elements[0:-1]

    premiers_elements.append(dernier_element)

    return "_".join(premiers_elements)


with codecs.open(INPUT_PATH, encoding='utf8') as input_file:
    if SKIP_FIRST_LINE:
        next(input_file)

    for line in input_file:
        fields = line.split(SEPARATOR)

        repo_url = fields[9]
        repo_url = repo_url.rstrip()

        student_name = fields[7]

        nom_etudiant = nettoyer_nom(student_name)

        nom_etudiant = prenom_en_premier(student_name)

        url_depot = inserer_mon_usager(repo_url)

        git_clone_command = "%s '%s' %s" % (GIT_CLONE, url_depot, nom_etudiant)

        print(git_clone_command)

        #os.system(git_clone_command)






