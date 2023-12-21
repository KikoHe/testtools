# -*- coding:utf-8 -*-

import unittest
from selenium import webdriver
from common


class PNB_Library(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'  # 设备系统
        desired_caps['platformVersion'] = '8.0.0'  # 设备系统版本
        desired_caps['deviceName'] = '3836414438313098'  # 设备名称
        desired_caps['appPackage'] = 'paint.by.number.pixel.art.coloring.drawing.puzzle'
        desired_caps['appActivity'] = 'com.meevii.business.splash.SplashActivity'
        desired_caps['unicodeKeyboard'] = True
        desired_caps['resetKeyboard'] = True
        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.driver.launch_app()
        self.driver.implicitly_wait(5)
        Install_gp_APK(self.driver)
        print ("Start library case")

    def tearDown(self):
        print ("end library case")
        print ("")
        self.driver.close_app()
        self.driver.implicitly_wait(5)