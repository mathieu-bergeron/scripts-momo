#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
#from selenium.webdriver.common.action_chains import ActionChains

import time
import re
import os
import argparse
import codecs
import yaml

parser = argparse.ArgumentParser(description='Extract answers from moodle quizz')
parser.add_argument('-grades', metavar='GRADES', default="grades.yaml", type=str, help='grades in .yaml format')
parser.add_argument('-destinations', metavar='DESTINATIONS', default="destinations.yaml", type=str, help='where to upload grades')
parser.add_argument('-c', metavar='COLNET', type=str, help='Colnet server name')
parser.add_argument('-u', metavar='USER', type=str, help='Colnet username')
parser.add_argument('-p', metavar='PASS', type=str, help='Colnet password')

args = parser.parse_args()

if args.grades is None or args.destinations is None \
   or args.c is None or args.u is None \
   or args.p is None:
    parser.print_usage()
    exit(0)

GRADES = args.grades
DESTINATION = args.destinations
COLNET_SERVER = args.c
USERNAME = args.u
PASSWORD = args.p

COLNET_URL = 'https://%s' % COLNET_SERVER
LOGIN_URL = '%s/login.asp' % COLNET_URL
LOGOUT_URL = '%s/logout.asp' % COLNET_URL

def logout(driver, logout_url):
    driver.get(logout_url)

def login(driver, login_url, username, password):
    driver.get(login_url)

    username_input = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('txtCodeUsager')) 
    username_input.send_keys(username)

    password_input = driver.find_element_by_id('txtMotDePasse')
    password_input.send_keys(password)

    login_button = driver.find_element_by_id('btnConnecter')
    login_button.click()


def open_quizz_attempts(driver, quizz_url):

    print(quizz_url)
    driver.get(quizz_url)

    anchor_divs = driver.find_elements_by_class_name('quizattemptcounts')
    if len(anchor_divs) > 0:
        anchor_div = anchor_divs[0]
        anchors = anchor_div.find_elements_by_tag_name('a')
        if len(anchors) > 0:
            anchor = anchors[0]
            driver.get(anchor.get_attribute('href'))

def extract_answer_urls_by_student_id(driver, quizz_url):
    answer_urls_by_student_id = dict({})

    open_quizz_attempts(driver, quizz_url)

    rows = driver.find_elements_by_xpath('//tbody/tr')

    for row in rows:
        user_ids = row.find_elements_by_class_name('c3')
        if len(user_ids) > 0:
            user_id = user_ids[0].text
            if id_matcher.match(user_id) is not None:
                print(user_id)
                answer_number = 9
                answer_cells = row.find_elements_by_class_name('c%s' % answer_number)
                while len(answer_cells) > 0:
                    answer_cell = answer_cells[0]
                    answer_anchors = answer_cell.find_elements_by_tag_name('a')
                    if len(answer_anchors) > 0:
                        answer_anchor = answer_anchors[0]
                        answer_url = answer_anchor.get_attribute('href')
                        if user_id in answer_urls_by_student_id:
                            answer_urls_by_student_id[user_id].append(answer_url)
                        else:
                            answer_urls_by_student_id[user_id] = list([answer_url])

                    answer_number += 1
                    answer_cells = row.find_elements_by_class_name('c%s' % answer_number)



    return answer_urls_by_student_id

def add_or_get(_dict, key, value):
    final_value = value

    if key in _dict:
        final_value = _dict[key]
    else:
        _dict[key] = final_value

    return final_value

def extract_answers(driver, answers, quizz_url, output_dirname):

    answer_urls_by_student_id = extract_answer_urls_by_student_id(driver, quizz_url)

    for user_id in answer_urls_by_student_id:

        answer_urls = answer_urls_by_student_id[user_id]

        for index, answer_url in enumerate(answer_urls):
            answer_name = "" + str(index + 1)
            answer_path = os.path.join(output_dirname, answer_name)

            current_answer = add_or_get(answers, answer_name, {})

            students = add_or_get(current_answer, 'students', {})

            current_student = add_or_get(students, user_id, {})

            if not os.path.exists(answer_path):
                os.mkdir(answer_path)

            output_path = os.path.join(answer_path, user_id + ".txt")

            current_student['_path'] = output_path

            add_or_get(current_student, 'grade', 0)
            add_or_get(current_student, 'comment', '')

            driver.get(answer_url)
            answer_divs = driver.find_elements_by_class_name('answer')

            output_text = ""

            if len(answer_divs) > 0:
                answer_div = answer_divs[0]
                answer_text = answer_div.text

                output_text += answer_text

            history_divs = driver.find_elements_by_class_name('history')
            if len(history_divs) > 0:
                output_text += "\n\n\n# Historique"
                history_div = history_divs[0]
                rows = history_div.find_elements_by_tag_name('tr')
                for index, row in enumerate(rows):
                    if index > 1 and index != (len(rows)-1):
                        rank_cell = row.find_elements_by_class_name('c0')[0]
                        time_cell = row.find_elements_by_class_name('c1')[0]
                        action_cell = row.find_elements_by_class_name('c2')[0]
                        output_text += "\n\n## Action " + rank_cell.text
                        output_text += "\n" + time_cell.text
                        output_text += "\n" + action_cell.text

            with codecs.open(output_path, 'w', encoding='utf8') as output_file:
                output_file.write(output_text)





if __name__ == '__main__':

    driver = webdriver.Firefox()

    login(driver, LOGIN_URL, USERNAME, PASSWORD)

    logout(driver, LOGOUT_URL)

    driver.quit()
