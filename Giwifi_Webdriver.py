# -*- coding:utf-8 -*-
# !/usr/bin/python3

#####################
# Author: Yuki Sui
# Date: 2022-5-4
#####################

# TODO: need rebuild, use protable firefox package --yukikawa


from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import re
import json
import time
import logfly

global phone, pwd


def gwifi_auth(phone, pwd):
    options = Options()
    options.headless = True

    wd = webdriver.Firefox(options=options)
    wd.implicitly_wait(10)
    wd.set_page_load_timeout(10)
    wd.get("http://down.gwifi.com.cn")
    # TODO: now gwifi login page has a alert, need process it --yukikawa

    # TODO: need rebuild, use new feature (By.id()) --yukikawa
    name_input = wd.find_element_by_id('first_name')
    pass_input = wd.find_element_by_id('first_password')
    login_button = wd.find_element_by_id('first_button')
    # TODO: need rebuild, use new feature (By.id()) --yukikawa
    name_input.clear()
    name_input.send_keys(phone)
    time.sleep(0.2)
    pass_input.clear()
    pass_input.send_keys(pwd)
    time.sleep(0.2)
    login_button.click()
    wd.implicitly_wait(4)
    # TODO: need use random delay --yukikawa

    wd.quit()
    print("All Done")


def get_info():
    try:
        file = open('config.pwd', 'r')
        js = file.read()
        dic = json.loads(js)
        phone = dic['phone']
        pwd = dic['pwd']
    except FileNotFoundError:
        phone = input('First use, please input your phone number: ')
        pwd = input('First use, please input your Gwifi password: ')
        dic = {'phone': phone, 'pwd': pwd}
        jsfile = json.dumps(dic)
        file = open('config.pwd', 'w')
        file.write(jsfile)
        file.close()
        file = open('config.pwd', 'r')
        js = file.read()
        file.close()
        dic = json.loads(js)
        phone = dic['phone']
        pwd = dic['pwd']
        print('success!')
    return phone, pwd


while True:
    phone = get_info()[0]
    pwd = get_info()[1]

    try:
        loginPage = requests.get('https://baidu.com', timeout=5).text
        time.sleep(10)
        pattern = re.compile("STATUS OK")
        if pattern.search(loginPage) is None:
            logfly.write_log('auth', 'fileCLI', 'error', 'Auth lost, try to re-Auth')
            gwifi_auth(phone, pwd)
            print('reconnected')
            logfly.write_log('auth', 'fileCLI', 'warning', 'Auth Commpleted!')
        else:
            logfly.write_log('auth', 'file', 'info', 'Already connected!')
    except:
        pass
