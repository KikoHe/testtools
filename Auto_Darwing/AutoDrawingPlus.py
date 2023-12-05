from appium import webdriver
desired_caps = {}
desired_caps['platformName'] = 'Android'  # 设备系统
desired_caps['platformVersion'] = '12'  # 设备系统版本
desired_caps['deviceName'] = 'R5CNC09S18K'  # 设备名称
# desired_caps['appPackage'] = 'com.vitastudio.color.paint.free.coloring.number'  # 包名
desired_caps['appPackage'] = 'com.android.settings'  # 包名
# desired_caps['appActivity'] = 'com.meevii.vitacolor.HomeActivity'  # 首页名
desired_caps['appActivity'] = 'com.android.settings.Settings'  # 首页名

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desired_caps)
print("启动设置应用")
driver.quit()