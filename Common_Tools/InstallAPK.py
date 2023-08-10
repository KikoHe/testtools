import os
os.system('adb devices')
os.system('adb uninstall happy.paint.coloring.color.number') #ZC
# os.system('adb uninstall paint.by.number.pixel.art.coloring.drawing.puzzle') #PBN
# os.system('adb uninstall holy.bible.biblegame.bibleverse.color.by.number.colorbynumber.paint.pixel.art') #BP

os.system('adb install -r /Users/ht/Downloads/colorFlow-v1.39.0-r1092-debug.apk')

os.system('adb logcat -c')
os.system('adb logcat -v time >/Users/ht/Downloads/log.txt')