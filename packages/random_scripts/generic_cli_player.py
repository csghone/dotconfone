#!/usr/bin/env python3

# Setup and Usage:
# - sudo -H pip3 install selenium`
# - Download geckodriver from https://github.com/mozilla/geckodriver/releases
# - export PATH=$PATH:<directory_of_geckodriver>`
# - python3 selenium_example.py

import os
import time
import getpass
import curses
import pickle

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def get_profile_dir(profile_name):
    profile_directory = os.path.expandvars(
        os.path.join("$HOME", ".cli_player", profile_name))
    if not os.path.exists(profile_directory):
        os.makedirs(profile_directory)
    return profile_directory

class Jango:
    LOGIN_LINK_ID = "splash_login_link"
    JANGO_LOGIN_LINK_ID = "j_login_button"
    USER_NAME = "email-input"
    PASSWORD = "username-input"
    PROFILE_DIR = get_profile_dir("jango")
    COOKIES = os.path.join(PROFILE_DIR, "cookies.pkl")

    options = Options()
    options.add_argument("--headless")
    fp = webdriver.FirefoxProfile(profile_directory=PROFILE_DIR)
    driver = webdriver.Firefox(firefox_profile=fp, options=options)
    driver.get("https://www.jango.com")
    if os.path.exists(COOKIES):
        for cookie in pickle.load(open(COOKIES, "rb")):
            driver.add_cookie(cookie)
    driver.get("https://www.jango.com")

    @staticmethod
    def is_logged_in():
        driver = Jango.driver
        try:
            play_button = driver.find_element_by_id("btn-playpause")
            return True
        except selenium.common.exceptions.NoSuchElementException:
            return False


    @staticmethod
    def login():
        driver = Jango.driver
        login_link = driver.find_element_by_id(Jango.LOGIN_LINK_ID)
        login_link.click()
        login_link = driver.find_element_by_id(Jango.JANGO_LOGIN_LINK_ID)
        login_link.click()
        login_field = driver.find_element_by_id(Jango.USER_NAME)
        login_field.clear() # Clear the text box
        login_field.send_keys(input("Username: "))
        login_field = driver.find_element_by_id(Jango.PASSWORD)
        login_field.clear() # Clear the text box
        login_field.send_keys(getpass.getpass() + Keys.ENTER)
        element = WebDriverWait(driver, 30).until(
            lambda x: x.find_element_by_id("btn-playpause"))
        pickle.dump(driver.get_cookies(), open(Jango.COOKIES,"wb"))

    @staticmethod
    def click_button(action):
        if action == "playpause":
            button_id = "btn-playpause"
        elif action == "next":
            button_id = "btn-ff"
        elif action == "prev":
            button_id = "btn-rewind"

        driver = Jango.driver
        button = driver.find_element_by_id(button_id)
        button.click()


    @staticmethod
    def get_display_info():
        driver = Jango.driver
        cur_song = driver.find_element_by_id("current-song")
        cur_artist = driver.find_element_by_id("player_current_artist")
        status = "{} {}".format(cur_song.text, cur_artist.text)
        return status

    @staticmethod
    def handle_keys(win):
        while True:
            key = win.getkey()
            if key == "q":
                break
            if key == "p":
                Jango.click_button("playpause")
                print(Jango.get_display_info(), "\n")
            if key == "n":
                Jango.click_button("next")
                print(Jango.get_display_info(), "\n")
            if key == "b":
                Jango.click_button("prev")
                print(Jango.get_display_info(), "\n")


if not Jango.is_logged_in():
    Jango.login()
time.sleep(5)
Jango.click_button("playpause")

driver = Jango.driver

curses.wrapper(Jango.handle_keys)
