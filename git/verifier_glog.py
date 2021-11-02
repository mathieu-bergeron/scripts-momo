#! /usr/bin/python
# vim: set fileencoding=utf-8 :
#
# --
# Copyright (C) (2019) (Mathieu Bergeron) (mathieu.bergeron@cmontmorency.qc.ca)
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

import subprocess
import re

NOMBRE_DE_LIGNES_APRES_APPEL=4

RECHERCHE='ag "\w+\s+\w+\s+\w+\s*\((\n|[^\)])*\)(\n|\s)*{$" --ignore-dir test --ignore-dir androidTest --ignore GLog.java -Gjava$ -A%d' % NOMBRE_DE_LIGNES_APRES_APPEL

resultat_chaine = subprocess.check_output(RECHERCHE, shell=True)

resultat_lignes = resultat_chaine.split('\n')

RE_PREFIXE_LIGNE='.*:\d+'
RE_LIGNE_METHODE=RE_PREFIXE_LIGNE + ':'
RE_LIGNE_APRES_METHODE=RE_PREFIXE_LIGNE + '-'
RE_LIGNE_GLOG=RE_PREFIXE_LIGNE + '-.*GLog\.appel'

re_ligne_methode = re.compile(RE_LIGNE_METHODE)
re_ligne_apres_methode = re.compile(RE_LIGNE_APRES_METHODE)
re_ligne_glog = re.compile(RE_LIGNE_GLOG)

lignes_methodes_a_verifier = []

lignes_methode = None
si_methode_lue = None
glog_trouve = None

def traiter_si_necessaire():
    global lignes_glog_manquant

    if si_methode_lue:
        if not glog_trouve:
            lignes_methodes_a_verifier.append(lignes_methode)

        reinitialiser()

def reinitialiser():
    global lignes_methode
    global si_methode_lue
    global glog_trouve

    lignes_methode = []
    si_methode_lue = False
    glog_trouve = False


reinitialiser()

for ligne in resultat_lignes:

    match_ligne_methode = re_ligne_methode.match(ligne)
    match_ligne_apres_methode = re_ligne_apres_methode.match(ligne)

    if match_ligne_methode is not None:
        traiter_si_necessaire()
        lignes_methode.append(ligne)

    elif match_ligne_apres_methode is not None:
        si_methode_lue = True

        match_ligne_glog = re_ligne_glog.match(ligne)
        if match_ligne_glog is not None:
            glog_trouve = True

traiter_si_necessaire()


if len(lignes_methodes_a_verifier) > 0:

    print "\n[Méthodes à vérifier pour GLog]\n"

    for lignes_methode in lignes_methodes_a_verifier:
        for ligne_methode in lignes_methode:
            print ligne_methode

        print ""

else:

    print "\n[Tout beau]\n"
