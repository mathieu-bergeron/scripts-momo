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
parser.add_argument('-exam', metavar='EXAM_NAME', type=str, help='exam name')
parser.add_argument('-destinations', metavar='DESTINATIONS', default="destinations.yaml", type=str, help='where to upload grades')
parser.add_argument('-c', metavar='COLNET', type=str, help='Colnet server name')
parser.add_argument('-u', metavar='USER', type=str, help='Colnet username')
parser.add_argument('-p', metavar='PASS', type=str, help='Colnet password')
parser.add_argument('--hide-comment', metavar='COMMENT', default=False, type=bool, help='Hide comment')

args = parser.parse_args()

if args.grades is None or args.destinations is None \
   or args.c is None or args.u is None \
   or args.p is None or args.exam is None:
    parser.print_usage()
    exit(0)

GRADES = args.grades
EXAM_NAME = args.exam
DESTINATIONS = args.destinations
COLNET_SERVER = args.c
USERNAME = args.u
PASSWORD = args.p
HIDE_COMMENT = args.hide_comment

COLNET_URL = 'https://%s' % COLNET_SERVER
LOGIN_URL = '%s/login.asp' % COLNET_URL
LOGOUT_URL = '%s/logout.asp' % COLNET_URL

def add_or_get(_dict, key, value):
    final_value = value

    if key in _dict:
        final_value = _dict[key]
    else:
        _dict[key] = final_value

    return final_value

def login(driver, login_url, username, password):
    driver.get(login_url)

    username_input = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('txtCodeUsager')) 
    username_input.send_keys(username)

    password_input = driver.find_element_by_id('txtMotDePasse')
    password_input.send_keys(password)

    login_button = driver.find_element_by_id('btnConnecter')
    login_button.click()

def logout(driver, logout_url):
    driver.get(logout_url)


def clear_field(field):
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)

def upload_grades(grades, exam_name, destinations):

    grades_link = driver.find_element_by_xpath('//td[@id="Menu02Center"]/a[@id="lnk"]')
    grades_link.click()

    for group_name in grades:

        full_group_name = destinations['groups'][group_name]['groupname']

        group_selector = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('cboClasse')) 
        group_selector.click()

        for option in group_selector.find_elements_by_tag_name('option'):
            if full_group_name in option.text:
                option.click()
                break

        input_grades_link = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//td[@width="14%"][3]/a')) 
        input_grades_link.click()

        exam_selector = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('cboCategTrav')) 
        exam_selector.click()

        full_eval_name = destinations['exams'][exam_name]['groups'][group_name]['evalname']

        for option in exam_selector.find_elements_by_tag_name('option'):
            if full_eval_name in option.text:
                option.click()
                break

        WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('chkPublierTravail')) 

        for student_id in grades[group_name]:
            grade = grades[group_name][student_id]['grade']
            comment_path = grades[group_name][student_id]['path']

            grade_input = driver.find_element_by_id("txtNoteSaisie20%s" % student_id)

            clear_field(grade_input)
            grade_input.send_keys("%.2f" % round(grade,2))

            grade_td = grade_input.find_element_by_xpath("..")
            grade_comment_link = grade_td.find_element_by_xpath("a")

            grade_comment_link.click()

            WebDriverWait(driver, 10).until(lambda x: x.window_handles[1]) 

            driver.switch_to.window(driver.window_handles[1])

            save_button = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('btnSauvegarder5')) 

            comment_area = driver.find_element_by_xpath('//textarea')
            comment_visible_checkbox = driver.find_element_by_id('chkCommentaireVisible')

            if HIDE_COMMENT:
                if comment_visible_checkbox.is_selected():
                    comment_visible_checkbox.click()
            else:
                if not comment_visible_checkbox.is_selected():
                    comment_visible_checkbox.click()

            clear_field(comment_area)

            with open(comment_path) as comment_file:
                comment_area.send_keys(comment_file.read())

            save_button.click()

            driver.switch_to.window(driver.window_handles[0])


        save_button = driver.find_element_by_id("btnSauvegarderSaisie5")
        save_button.click()

        # there seem to be a limit to how quick 
        # we can save a second page
        time.sleep(3)




if __name__ == '__main__':

    driver = webdriver.Firefox()

    login(driver, LOGIN_URL, USERNAME, PASSWORD)

    with open(GRADES) as yaml_grades_file:
        grades = yaml.load(yaml_grades_file.read(), Loader=yaml.FullLoader)
        if grades is None:
            grades = {}

    with open(DESTINATIONS) as yaml_destinations_file:
        destinations = yaml.load(yaml_destinations_file.read(), Loader=yaml.FullLoader)
        if destinations is None:
            destinations = {}

    upload_grades(grades, EXAM_NAME, destinations)

    time.sleep(2)

    logout(driver, LOGOUT_URL)

    driver.quit()
