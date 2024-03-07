#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8
__author__='kiko'

'''测试前的准备相关工具'''

import subprocess

def install_apk(apk_path):
    result = subprocess.run(["adb", "install", "-r", apk_path], capture_output=True, text=True)
    print(result.stdout)

def uninstall_apk(project):
    backage_name = {
        "BP":"holy.bible.biblegame.bibleverse.color.by.number.colorbynumber.paint.pixel.art",
        "PBN":"",
        "ZC":"happy.paint.coloring.color.number",
        "VC":"com.vitastudio.color.paint.free.coloring.number"
    }
    result = subprocess.run(["adb", "uninstall", backage_name[project]], capture_output=True, text=True)
    print(result.stdout)

uninstall_apk("VC")
