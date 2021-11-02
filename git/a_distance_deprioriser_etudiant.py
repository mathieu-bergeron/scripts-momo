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

PRIORITE_PATH='les_priorites.json'

liste_priorite = []


def deprioriser_etudiant(numero):

    if numero not in liste_priorite:
        print "[ERREUR] étudiant non-trouvé %s" % numero
        return

    liste_priorite.remove(numero)
    liste_priorite.append(numero)


if __name__ == '__main__':

    numero = ""

    if len(sys.argv) == 2:
        numero = sys.argv[1]
    else:
        print "usage: python %s NUMERO_ETUDIANT" % sys.argv[0]

    with codecs.open(PRIORITE_PATH, encoding='utf8') as fichier_priorites:
        liste_priorite = json.loads(fichier_priorites.read())

    deprioriser_etudiant(numero)

    with codecs.open(PRIORITE_PATH, 'w', encoding='utf8') as fichier_priorites:
        fichier_priorites.write(json.dumps(liste_priorite, indent=4, ensure_ascii=False))
