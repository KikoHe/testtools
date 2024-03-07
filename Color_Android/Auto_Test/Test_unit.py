#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
__author__='kiko'
from selenium.webdriver.common.by import By

'''description:UI公共类'''
def isExistElementByID(driver, ele_id):
    """
    :Usage: 使用id判断元素是否存在
    :param driver: Page Object
    :param ele_id: 元素的id属性
    :return: boolean value,若存在则为true，否则为false
    """
    try:
        driver.find_element_by_id(ele_id)
        return True
    except:
        return False

def clickbyid(driver, ele_id):
    driver.find_element(By.ID, ele_id).click()
