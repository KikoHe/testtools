# -*- coding:utf-8 -*-
import time
from appium import webdriver
from selenium.common import TimeoutException
from Test_unit import *

desired_caps = {}
desired_caps['platformName'] = 'Android'  # 设备系统
desired_caps['platformVersion'] = '9'  # 设备系统版本
desired_caps['deviceName'] = '9887bc464f3239444d'  # 设备名称
desired_caps['appPackage'] = 'com.vitastudio.color.paint.free.coloring.number'
desired_caps['appActivity'] = 'com.meevii.vitacolor.HomeActivity'
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
time.sleep(15)
try:
    isExistElementByID(driver, "com.vitastudio.color.paint.free.coloring.number:id/bottom_sheet")\
        or isExistElementByID(driver, "com.vitastudio.color.paint.free.coloring.number:id/vc_logo")
    print("Launch success~")
except TimeoutException:
    print("Error")
driver.quit()
