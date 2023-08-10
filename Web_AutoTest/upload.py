#! /usr/bin/python3
from time import sleep

import pyperclip
from pykeyboard import PyKeyboard
from pymouse import PyMouse
from selenium import webdriver
from selenium.webdriver.common.by import By
from torch import get_file_path

driver = webdriver.Chrome()
url = "https://cms-test.colorflow.app/#/collect"
driver.get(url)
# 等待30秒,登录账户
sleep(20)
driver.find_element(By.XPATH, "/HTML/body/section/section/section/aside/div/ul/li[3]/div").click()
sleep(1)
driver.find_element(By.XPATH, "/HTML/body/section/section/section/aside/div/ul/li[3]/ul/li[2]").click()
sleep(3)
driver.find_element(By.XPATH, "/HTML/body/section/section/section/main/div/div[2]/div/div/div[1]/div[1]/div[3]/table/tbody/tr[1]/td[6]/div/button/span").click()
sleep(3)
driver.find_element(By.XPATH, "/HTML/body/section/section/section/main/div/div[2]/div/div/div[2]/div/div[2]/form/div[5]/div/div/div/div/div[1]/div/button/span").click()

k = PyKeyboard()
m = PyMouse()
filepath = "//pythonProject/DownloadResource/ios/Lake.zip"
k.press_keys(['Command', 'Shift', 'G'])
x_dim, y_dim = m.screen_size()
m.click(x_dim // 2, y_dim // 2, 1)
# 复制文件路径开头的斜杠/，如果不加斜杠的话，脚本会缺少头部的斜杠
pyperclip.copy(filepath)
# 粘贴斜杠/
k.press_keys(['Command', 'V'])
sleep(1)
k.press_key('Return')
sleep(1)
k.press_key('Return')
sleep(10)
# # 退出浏览器
# driver.quit()