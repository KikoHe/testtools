# -*- coding:utf-8 -*-

import json
import requests
from src.common.Draw_unit import *
from src.pages.drawing_pages import *
desired_caps = {}
desired_caps['platformName'] = 'iOS'  # 设备系统
desired_caps['platformVersion'] = '12.2'  # 设备系统版本
desired_caps['deviceName'] = 'iPhone 6s'  # 设备名称
desired_caps['app'] = '/Users/apple/Desktop/pbn_autotest_ios_pyton3/app/PaintByNumber.app'
desired_caps['automationName'] = 'XCUITest'
desired_caps['noReset'] = True  #重置应用，清楚数据
desired_caps['locale'] = 'fr_US'  #设置系统地区，区分国内国际版本
driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)



response = requests.get("http://paint-api.dailyinnovation.biz/paint/v1/paint/5d1567f3cd5f400001657d6d")
js = json.loads(response.text)
def get_url(url_id):
    url = 'http://paint-api.dailyinnovation.biz/paint/v1/paint/{code}'.format(code = url_id)
    response = requests.get(url)
    return response
js = json.loads(get_url('5bbf251ba28896000192b651').text)
data = js["data"]
plan = data["plans"]
center = data["center"]
type = data["type"]
plan_number = plan[0].split('|')  #色号数
print(str(len(plan_number))+"个色号")
color_number = center.split('|')  #色块数
print(str(len(color_number))+"个色快")

def plan_number_code_test(i):
    '''列表形式返回第i个色号的所有色块'''
    plan_number_code = plan_number[i].split('#')
    plan_number_code_test = plan_number_code[0].split(',')
    return plan_number_code_test

def color_number_code(i):
    '''列表形式返回第i个色块的基本信息'''
    color_number_code = color_number[i].split(',')
    return color_number_code

def xx(a,b):
    '''
    :param a:第几个色号
    :param b:该素材第几个色块
    :return: 返回该色块x坐标
    '''
    if a < len(plan_number):
        for i in range(len(color_number)):
            if plan_number_code_test(a)[b] == color_number_code(i)[0]:
                # print(color_number_code(i)[1])
                break
    return color_number_code(i)[1]

def yy(a, b):
    '''
    :param a:第几个色号
    :param b:该素材第几个色块
    :return: 返回该素材y坐标
    '''
    if a < len(plan_number):
        for i in range(len(color_number)):
            if plan_number_code_test(a)[b] == color_number_code(i)[0]:
                # print(color_number_code(i)[2])
                break
    return color_number_code(i)[2]

def color_type(driver,pic_path):
    w = int(driver.find_element_by_xpath(pic_path).size['width'])
    h = int(driver.find_element_by_xpath(pic_path).size['height'])
    print(w, h)
    a = 0
    while a < len(plan_number):
        b = 0
        while b < len(plan_number_code_test(a)):
            x = int(xx(a, b))
            y = int(yy(a, b))
            if type == "normal":
                location = (int(x/1024*w), int(y/1024*w)+(h-w)/2)
            elif type == "colored":
                location = (int(x/2048*w), int(y/2048*w)+(h-w)/2)
            print(location)
            driver.implicitly_wait(3)
            driver.tap([(location)], 1000)
            driver.implicitly_wait(3)
            b = b + 1
            if b >= len(plan_number_code_test(a)):
                print("color one number...")
                break
                ele = driver.find_element_by_ios_predicate('name = "{code}"').format(code = a+1)
                if ele:
                    driver.get_screenshot_as_file("/Users/apple/Desktop/pbn_autotest_ios_pyton3/screenshot/error.png")
        a = a + 1

path = '//XCUIElementTypeApplication[@name="Paint By Number"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther'
path1 = '//XCUIElementTypeApplication[@name="Paint By Number"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[1]'
driver.implicitly_wait(30)
driver.find_element_by_xpath(path).click()
draw_view_action(driver,3)
driver.implicitly_wait(3)
color_type(driver,path1)