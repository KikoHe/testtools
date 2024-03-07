#!/bin/sh

am start -n paint.by.number.pixel.art.coloring.drawing.puzzle/com.meevii.business.splash.SplashActivity
adb logcat | grep "adsdk_core_init" > log_file.txt
