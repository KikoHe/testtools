# -*- coding:utf-8 -*-
import unittest
from appium import webdriver
from PBN_teststep import *
class VC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'  # 设备系统
        desired_caps['platformVersion'] = '12'  # 设备系统版本
        desired_caps['deviceName'] = 'R5CNC09S18K'  # 设备名称
        desired_caps['appPackage'] = 'paint.by.number.pixel.art.coloring.drawing.puzzle'
        desired_caps['appActivity'] = 'com.meevii.business.splash.SplashActivity'
        desired_caps['app'] = '/Users/ht/Downloads/PBN--v4.6.7-r10983-release.apk'  # 应用程序的本地路径

        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        driver = self.driver
        # driver.activate_app('com.vitastudio.color.paint.free.coloring.number')
        # time.sleep(3)
        # element_disappear_by_id(driver, "vc_logo")

    def tearDown(self):
        ...
        # self.driver.terminate_app('com.vitastudio.color.paint.free.coloring.number')

    def test_case_3(self):
        driver = self.driver
        while True:
            status = test(driver)
            if status == "false":
                break
            else:
                driver.remove_app('paint.by.number.pixel.art.coloring.drawing.puzzle')
                driver.install_app('/Users/ht/Downloads/PBN--v4.6.7-r10983-release.apk')
                time.sleep(5)
                driver.activate_app('paint.by.number.pixel.art.coloring.drawing.puzzle')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(VC("test_case_3"))
    runner = unittest.TextTestRunner()
    runner.run(suite)





