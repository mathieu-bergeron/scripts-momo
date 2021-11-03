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

def add_or_get(_dict, key, value):
    final_value = value

    if key in _dict:
        final_value = _dict[key]
    else:
        _dict[key] = final_value

    return final_value

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





if __name__ == '__main__':

    driver = webdriver.Firefox()

    login(driver, LOGIN_URL, USERNAME, PASSWORD)

    logout(driver, LOGOUT_URL)

    driver.quit()
