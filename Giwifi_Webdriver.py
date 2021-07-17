# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time

def GwifiAuth():
    phone = 'your phone' #change to your phone
    pwd = 'your pwd' #change to your pwd
    options = Options()
    options.headless = True
    
    wd = webdriver.Firefox(options=options)
    wd.implicitly_wait(10)
    wd.set_page_load_timeout(10)
    wd.get("link which can redirect to Giwifi login page")  #change to link which can redirect to Giwifi login page

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

    print ("All Done")
    exit()

if __name__ == "__main":
    GwifiAuth()