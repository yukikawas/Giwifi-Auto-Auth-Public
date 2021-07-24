# -*- coding:utf-8 -*-
# !/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import requests
import re
import time

phone = 'your phone'
pwd = 'your pwd'


def GwifiAuth():
    options = Options()
    options.headless = True

    wd = webdriver.Firefox(options=options)
    wd.implicitly_wait(10)
    wd.set_page_load_timeout(10)
    wd.get("http://172.16.1.1:8062/redirect")
    # wd.maximize_window()

    """这段可以查看selenium的源码,属于smart wait"""
    name_input = wd.find_element_by_id('first_name')  # 找到用户名的框框
    pass_input = wd.find_element_by_id('first_password')
    login_button = wd.find_element_by_id('first_button')
    name_input.clear()
    name_input.send_keys(phone)  # 填写用户名
    time.sleep(0.2)
    pass_input.clear()
    pass_input.send_keys(pwd)  # 填写密码
    time.sleep(0.2)
    login_button.click()  # 点击登录
    wd.implicitly_wait(4)
    wd.quit()
    print("All Done")


def writelog(info):
    times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    LogFile = open('GwifiAuth.log', 'a')
    LogFile.write(times + ' ' + info + '\r\n')
    LogFile.close()


while True:
    try:
        loginPage = requests.get('https://baidu.com', timeout=5).text
        time.sleep(10)
        pattern = re.compile("STATUS OK")
        if pattern.search(loginPage) == None:
            writelog('Auth lost, try to re-Auth')
            GwifiAuth()
            print('reconnected')
            writelog('Auth commpleted!')
        else:
            writelog('Already connected')
    except:
        pass