# -*- coding:utf-8 -*-

import unittest
from appium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from Common_action import *

class VC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'  # 设备系统
        desired_caps['platformVersion'] = '9'  # 设备系统版本
        desired_caps['deviceName'] = '9887bc464f3239444d'  # 设备名称
        desired_caps['appPackage'] = 'com.vitastudio.color.paint.free.coloring.number'
        desired_caps['appActivity'] = 'com.meevii.vitacolor.HomeActivity'
        # desired_caps['unicodeKeyboard'] = True
        # desired_caps['resetKeyboard'] = True
        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_CheckAPPOpenSuccess(self):
        try:
            # 等待直到元素可见，或者超时抛出TimeoutException异常
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.ID, "com.vitastudio.color.paint.free.coloring.number/tv_sure"))
            )
            print("元素加载完成。")
        except TimeoutException:
            print(f"等待超过30秒后元素未出现。")

if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(VC("test_CheckAPPOpenSuccess"))
    runner = unittest.TextTestRunner()
    runner.run(suite)