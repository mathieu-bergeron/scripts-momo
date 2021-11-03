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

codes = []

ID_PATTERN="[0-9]{7}"
id_matcher = re.compile(ID_PATTERN)

parser = argparse.ArgumentParser(description='Extract answers from moodle quizz')
parser.add_argument('-d', metavar='YAML_DB', default="db.yaml", type=str, help='.yaml DB')
parser.add_argument('-m', metavar='MOODLE', type=str, help='Moodle server')
parser.add_argument('-u', metavar='USER', type=str, help='Moodle username')
parser.add_argument('-p', metavar='PASS', type=str, help='Moodle password')
parser.add_argument('-q', metavar='URL', type=str, help='quizz URL path')
parser.add_argument('-e', metavar='EXAM_NAME', type=str, help='Exam name')
parser.add_argument('--max-grade', metavar='MAX_GRADE', default="10", type=str, help='Exam name')
parser.add_argument('-o', metavar='OUTDIR', type=str, help='Output dir')

args = parser.parse_args()

if args.d is None or args.u is None \
   or args.p is None or args.m is None \
   or args.q is None or args.o is None \
   or args.e is None or args.max_grade is None:
    parser.print_usage()
    exit(0)

YAML_DB = args.d
EXAM_NAME = args.e
SERVER_NAME = args.m
QUIZZ_PATH = args.q
USERNAME = args.u
PASSWORD = args.p
OUTPUT_DIRNAME = args.o
MAX_GRADE = args.max_grade

MOODLE_URL = 'https://%s' % SERVER_NAME
LOGIN_URL = "%s/login/index.php" % MOODLE_URL
QUIZZ_URL = "%s/%s" % (MOODLE_URL, QUIZZ_PATH)

def login(driver, login_url, username, password):
    driver.get(login_url)

    username_input = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('username')) 
    username_input.send_keys(username)

    password_input = driver.find_element_by_id('password')
    password_input.send_keys(password)

    login_button = driver.find_element_by_id('loginbtn')
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

    db = {}

    if os.path.exists(YAML_DB):
        with open(YAML_DB) as yaml_db_file:
            db = yaml.load(yaml_db_file.read(), Loader=yaml.FullLoader)
            if db is None:
                db = {}


    exam = add_or_get(db, EXAM_NAME, {})

    exam['max_grade'] = MAX_GRADE

    answers = add_or_get(exam, 'answers', {})

    driver = webdriver.Firefox()

    login(driver, LOGIN_URL, USERNAME, PASSWORD)

    if not os.path.exists(OUTPUT_DIRNAME):
        os.makedirs(OUTPUT_DIRNAME)

    extract_answers(driver, answers, QUIZZ_URL, OUTPUT_DIRNAME)

    driver.close()

    with open(YAML_DB, 'w') as yaml_db_file:
        yaml_db_file.write(yaml.dump(db))

    yaml_content = ""

    comment_matcher = re.compile("^(\s*)(comment:)(.*)$")

    with open(YAML_DB) as yaml_db_file:
        for yaml_line in yaml_db_file:
            comment_match = comment_matcher.match(yaml_line)
            if comment_match is not None and "''" in comment_match.group(3):
                yaml_line = comment_match.group(1) + comment_match.group(2) + "\n"
                yaml_line += comment_match.group(1) + "  |\n"

            yaml_content += yaml_line

    with open(YAML_DB, 'w') as yaml_db_file:
        yaml_db_file.write(yaml_content)
