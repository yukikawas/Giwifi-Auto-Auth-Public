# -*- coding:utf-8 -*-
# !/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import re
import json
import time

global phone, pwd


def gwifi_auth(phone, pwd):
    options = Options()
    options.headless = True

    wd = webdriver.Firefox(options=options)
    wd.implicitly_wait(10)
    wd.set_page_load_timeout(10)
    wd.get("http://down.gwifi.com.cn")

    name_input = wd.find_element_by_id('first_name')
    pass_input = wd.find_element_by_id('first_password')
    login_button = wd.find_element_by_id('first_button')
    name_input.clear()
    name_input.send_keys(phone)
    time.sleep(0.2)
    pass_input.clear()
    pass_input.send_keys(pwd)
    time.sleep(0.2)
    login_button.click()
    wd.implicitly_wait(4)
    wd.quit()
    print("All Done")


def writelog(info):
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_file = open('GwifiAuth.log', 'a')
    log_file.write(times + ' ' + info + '\r\n')
    log_file.close()


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


while True:  # TODO use daemon instead of while true
    phone = get_info()[0]
    pwd = get_info()[1]

    try:
        loginPage = requests.get('https://baidu.com', timeout=5).text
        time.sleep(10)
        pattern = re.compile("STATUS OK")
        if pattern.search(loginPage) == None:
            writelog('Auth lost, try to re-Auth')
            gwifi_auth(phone, pwd)
            print('reconnected')
            writelog('Auth completed!')
        else:
            writelog('Already connected')
    except:
        pass
