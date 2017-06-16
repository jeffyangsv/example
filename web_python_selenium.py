# -*- coding: utf-8 -*-


import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
  
chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
  
driver = webdriver.Chrome(chromedriver)
driver.get("http://172.16.77.160:8080/")
assert "XORMEDIA" in driver.title  
user = driver.find_element_by_name("user_id")
user.send_keys("su")
elem_pwd = driver.find_element_by_name("password")
elem_pwd.send_keys("su")
elem_pwd.send_keys(Keys.RETURN)
try:
    if driver.find_element_by_id('_PM'):
        driver.find_element_by_id('_PM').click()
except:
    print('can not find PM')
try:
    if driver.find_element_by_xpath('//*[@id="_label"]/tbody/tr[3]/td/a/img'):
        driver.find_element_by_xpath('//*[@id="_label"]/tbody/tr[3]/td/a/img').click()
except:
    print('can not enter PM')

driver.switch_to_frame('left')
driver.switch_to_frame('leftMainFrame')
try:
    if driver.find_element_by_xpath('/html/body/form/table[1]/tbody/tr[3]/td/a'):
        driver.find_element_by_xpath('/html/body/form/table[1]/tbody/tr[3]/td/a').click()
except:
    print('can not open 电子节目单列表')
print(driver.find_element_by_xpath('/html/body/form/table[1]/tbody/tr[3]/td/a').text)
driver.switch_to_default_content()
driver.switch_to_frame('frameb')
driver.switch_to_frame('mainFrame_b')
try:
    if driver.find_element_by_xpath('//*[@id="objSearchCondition"]/tbody/tr[1]/td[2]/select/option[18]'):
        driver.find_element_by_xpath('//*[@id="objSearchCondition"]/tbody/tr[1]/td[2]/select/option[18]').click()
except:
    print('can not open CCTV1')
driver.find_element_by_xpath('//*[@id="objSearchCondition"]/tbody/tr[1]/td[4]/a').click()    
       
assert "test" in driver.title   
driver.close()  
driver.quit()

 