#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
__author__='kiko'

'''description:UI公共类'''

import os

def Install_gp_APK(driver):
    '''安装google play 包'''
    while not isExistElementByID(driver,"item_3"):
        driver.remove_app("paint.by.number.pixel.art.coloring.drawing.puzzle")
        driver.install_app(get_gp_app())
        print ("install : " + get_gp_app())
        driver.launch_app()
        driver.implicitly_wait(3)
        before_test(driver)
    print ("this is gp Apk")

def Allow_box(driver):
    '''allow 授权弹框'''
    while isExistElementByID(driver,"com.android.packageinstaller:id/permission_allow_button"):
        driver.find_element_by_id("com.android.packageinstaller:id/permission_allow_button").click()
        driver.implicitly_wait(3)

def get_gp_app():
    '''获取gp apk'''
    for dir,redir,files in os.walk(gl.test_apk):
        i = 1
        while i < len(files):
            if len(files[i]) <= 23 :
                l = []
                l.append(files[i])
            i = i + 1
    print(l)
    return (gl.test_apk + l[-1])
