# -*- coding:utf-8 -*-
import unittest
from appium import webdriver
from TestStep import *

class VC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'  # 设备系统
        desired_caps['platformVersion'] = '12'  # 设备系统版本
        desired_caps['deviceName'] = 'R5CNC09S18K'  # 设备名称
        desired_caps['appPackage'] = 'com.vitastudio.color.paint.free.coloring.number'
        desired_caps['appActivity'] = 'com.meevii.vitacolor.HomeActivity'
        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)

        click_by_id(cls.driver, "btn_text", "bottom_sheet")
        if int(desired_caps['platformVersion']) >= 13:
            print("system >= 13")
            click_by_id(cls.driver, "com.android.permissioncontroller:id/permission_allow_button")
        Open_Debug_Funtion(cls.driver)
        # remove_directory("/screenshots")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        driver = self.driver
        driver.activate_app('com.vitastudio.color.paint.free.coloring.number')
        time.sleep(3)
        element_disappear_by_id(driver, "vc_logo")

    def tearDown(self):
        self.driver.terminate_app('com.vitastudio.color.paint.free.coloring.number')

    def test_case_1(self):
        ###完成Daily素材，并检查reward广告
        driver = self.driver

        click_by_id(driver, "tab_daily")
        click_by_id(driver, "img_item")
        element_appear_by_id(driver, "tips")
        long_press_until_alert(driver, "tips", "fill_all", timeout=10)
        input_by_id(driver, "etHint", "0")
        driver.press_keycode(4)
        element_disappear_by_id(driver, "etHint")
        while get_element_attribute_by_id(driver, "tips", "enabled", timeout=10) == "false":
            time.sleep(3)
            if get_element_attribute_by_id(driver, "tips", "enabled", timeout=10) == "ture":
                break
        click_by_id(driver, "tips")
        Check_Close_AD(driver)
        Fill_Pic(driver)
        Close_Finish(driver)
        element_appear_by_id(driver, "img_item")
        take_screenshot_and_save(driver, save_path="/screenshots", file_name="Finish_Daily_Pic")
        time.sleep(5)

    def test_case_2(self):
        ###完成全部图库页当天更新的素材，并检查插屏广告
        driver = self.driver
        element_appear_by_id(driver, "start_top_tag")  # 确认元素首次出现
        pic_num = 0
        while True:  # 开始一个循环
            new_pic_elements = find_all_new_pic(driver, "start_top_tag")
            if not new_pic_elements:  # 如果没有找到元素
                swipe(driver, "down")  # 滑动页面的函数
                new_pic_elements = find_all_new_pic(driver, "start_top_tag")  # 再次检查新元素
                if not new_pic_elements:  # 如果滑动后仍然没有找到元素，退出循环
                    break
            for pic in new_pic_elements:
                pic.click()
                Check_Close_AD(driver)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "btnExit")))  # 使用显式等待代替time.sleep
                Fill_Pic(driver)
                Close_Finish(driver)
                Close_RatausDialog(driver)
                Close_Garden_Guide(driver)
                element_appear_by_id(driver, "library_root")
            take_screenshot_and_save(driver, save_path="/screenshots", file_name="Finish_Library_Pic")
        print("Finish all new lib pic.")

if __name__=='__main__':
    suite = unittest.TestSuite()
    suite.addTest(VC("test_case_1"))
    suite.addTest(VC("test_case_2"))
    runner = unittest.TextTestRunner()
    runner.run(suite)