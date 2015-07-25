#!/usr/bin/env python
# -*- coding: utf-8 -*-
from docutils.parsers.rst.directives import body

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.errorhandler import NoSuchElementException

class cyberghostvpn():
    def __init__(self):
        self.url_login = 'https://account.cyberghostvpn.com/en_us/login'
        # self.user_name = 'ghbphfr1'
        # self.passwd = 'wdcxz321'
        self.response_timeout = 5
        self.max_script_run = 5
        self.page_load_timeout = 20
        self.impl_wait = 10

        self.elements = dict(login=".//*[@id='loginForm']/input[1]",
                             passwd=".//*[@id='loginForm']/input[2]",
                             button_login=".//*[@id='loginForm']/button",
                             show_keys_form=".//*[@id='account']/div[1]/div[2]/div[1]/div[3]/div/a",
                             input_key=".//*[@id='account']/div[1]/div[2]/div[2]/div[2]/input",
                             button_key=".//*[@id='account']/div[1]/div[2]/div[2]/div[3]/button[1]",
                             alert_text=".//*[@id='ng-app']/body/div[4]/div/div/div[1]/h3",
                             alert_button=".//*[@id='ng-app']/body/div[4]/div/div/div[3]/button",
                             activation_button=".//*[@id='ng-app']/body/div[4]/div/div/div[3]/button[1]",
                             plan_text=".//*[@id='account']/div[1]/div[2]/div[1]/div[2]")

        self.result_text = dict(not_found="Activation key not found",
                                activated="Activation key already used",
                                done="Activate your subscriptio")

        self.plan_text = ("Free Plan", "Premium")

        self.start_browser()
        #self.driver.maximize_window()

    def start_browser(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("http.response.timeout", self.response_timeout)
        fp.set_preference("dom.max_script_run_time", self.max_script_run)
        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.set_page_load_timeout(self.page_load_timeout)
        self.driver.implicitly_wait(self.impl_wait)

    def __del__(self):
        self.driver.close()

    def wait_element(self, xpath):
        trigger = False
        while not trigger:
            try:
                element = self.driver.find_element_by_xpath(xpath)
            except NoSuchElementException:
                trigger = False
            else:
                trigger = True
        return element

    def load_end(self, msg):
        while not (self.driver.title.startswith(msg)):
            pass
        return True

    def get_alertion_text(self):
        self.wait_element(self.elements["alert_text"])
        alert_text = self.driver.find_element_by_xpath(self.elements["alert_text"]).text

        if self.result_text["activated"] in alert_text:
            button = self.wait_element(self.elements["activation_button"])
        else:
            button = self.wait_element(self.elements["alert_button"])
        button.click()
        plan_text = self.wait_element(self.elements["plan_text"])
        return (self.plan_text[1] in plan_text.text)

    def login(self, user_name, user_passwd):
        self.driver.get(self.url_login)
        login = self.driver.find_element_by_xpath(self.elements['login'])
        passwd = self.driver.find_element_by_xpath(self.elements['passwd'])
        button = self.driver.find_element_by_xpath(self.elements['button_login'])

        login.send_keys(user_name)
        passwd.send_keys(user_passwd)
        button.click()
        self.load_end('Management')
        return True

    def key_input_activate(self):
        show_form = self.wait_element(self.elements['show_keys_form'])
        show_form.send_keys(Keys.RETURN)
        return True

    def check_key(self, key):
        key_input = self.driver.find_element_by_xpath(self.elements['input_key'])
        button = self.driver.find_element_by_xpath(self.elements['button_key'])

        key_input.clear()
        key_input.send_keys(key)

        try:
            button.click()
        except:
            self.driver.execute_script('window.stop();')

    def get_plan(self):
        plan = self.driver.find_element_by_xpath(self.elements["plan_text"]).text
        return plan

    def reload(self):
        self.driver.close()
        self.start_browser()

# cg = cyberghostvpn()
# cg.login('ghbphfr1', 'wdcxz321')
# plan = cg.get_plan()
# print plan
# cg.key_input_activate()
# cg.check_key('CHZ-NP3KF-9NQWS-2HTS7-LVPGQ-XHTR6')
# print (cg.plan_text[1] in plan)
# input('Press any key...')
# cg.destroy()
