#! /usr/bin/python
# vim: set fileencoding=utf8 :
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
import os
import sys
import re

# IMPORANT: input files must be UTF-8 
#           use e.g. vim with :set fileencoding=utf8 :w
#INPUT_PATH='4205B5MO-000002.csv'
#OUTPUT_PATH='noms2.html' 

if len(sys.argv) <= 1:
    print "usage %s in.csv {hauteur_ligne}"
    exit(0)

INPUT_PATH=sys.argv[1]
GROUPE = int(INPUT_PATH.split('-')[1].split('.')[0])
HAUTEUR_LIGNE=34
try:
    HAUTEUR_LIGNE=sys.argv[3]
except:
    pass

OUTPUT_PATH='groupe%02d.html' % GROUPE

SKIP_FIRST_LINE=True

SEPARATOR=';'
COMMENT='#'

NOMBRES_COLONNES_VIDES=9

ATELIER='TP'


def entetes_vides(output, nombre):
    for x in xrange(nombre):
        output.write("<th width='300px'>")
        output.write("&nbsp;")
        output.write("</th>")

def cases_vides(output, nombre):
    for x in xrange(nombre):
        output.write("<td>")
        output.write("&nbsp;")
        output.write("</td>")

def get_initiales(nom_de_famille):
    return "".join([ x for x in nom_de_famille if x.isupper() ])


def rangee(out, numero, prenom, initiales, si_couleur):
    if si_couleur:
        style="style='background-color:lightgray;' bgcolor='#DCDCDC'"
    else:
        style=""

    out.write( "<tr height='%s px' %s>\n" % (HAUTEUR_LIGNE, style))
    out.write( "<td %s>" % style)
    out.write(numero)
    out.write( "</td>")
    out.write( "<td %s>" % style)
    out.write(prenom)
    out.write( "</td>")
    out.write( "<td %s>" % style)
    out.write(initiales)
    out.write( "</td>")
    cases_vides(out, NOMBRES_COLONNES_VIDES+1)
    out.write( "</tr>")

def process(INPUT_PATH, OUTPUT_PATH):


    with codecs.open(OUTPUT_PATH, 'w', encoding='utf8') as output_file:
        if 'html' in OUTPUT_PATH:
            output_file.write(" <meta charset='UTF-8'>\n")
            output_file.write(" <head><style>table,tr,th,td {border: 1px solid black; border-collapse: collapse;} </style>\n")
            # FIXME: il faudrait une marge en fait
            output_file.write("<br>\n")
            output_file.write("<h3>Groupe %02d, %s <u>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</u> </h3>\n" % (GROUPE, ATELIER))
            output_file.write("<table>\n")
            output_file.write("<tr>\n")
            output_file.write("<th>")
            output_file.write(u"numéro")
            output_file.write("</th>")
            output_file.write("<th>")
            output_file.write(u"prénom")
            output_file.write("</th>")
            output_file.write("<th>")
            output_file.write("nom")
            output_file.write("</th>")
            entetes_vides(output_file, NOMBRES_COLONNES_VIDES)
            #output_file.write("<th>")
            #output_file.write("/100")
            #output_file.write("</th>")
            output_file.write("<th>")
            output_file.write(u"validé")
            output_file.write("</th>")
            output_file.write("</tr>")


        with codecs.open(INPUT_PATH, encoding='ISO-8859-1') as input_file:
            if SKIP_FIRST_LINE:
                next(input_file)

            linenum = 0

            for (i, line) in enumerate(input_file):
                if line.startswith(COMMENT):
                    continue
                else:
                    linenum += 1

                fields = line.split(SEPARATOR)
                name = fields[1]
                numero = fields[2]
                if numero.startswith('20'):
                    numero = numero[2:]

                surname = fields[0]

                initiales = get_initiales(surname)

                if 'html' in OUTPUT_PATH:
                    rangee(output_file, numero, name, initiales, linenum%2==0)

                if 'html' not in OUTPUT_PATH:
                    output_file.write( numero + " " + name+" "+surname)
                    output_file.write("\n")


        if 'html' in OUTPUT_PATH:
            output_file.write( "</table>\n")


process(INPUT_PATH, OUTPUT_PATH)
