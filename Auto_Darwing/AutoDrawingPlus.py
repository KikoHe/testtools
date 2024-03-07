from appium import webdriver
desired_caps = {}
desired_caps['platformName'] = 'Android'  # 设备系统
desired_caps['platformVersion'] = '9'  # 设备系统版本
desired_caps['deviceName'] = '9887bc464f3239444d'  # 设备名称
desired_caps['appPackage'] = 'com.vitastudio.color.paint.free.coloring.number'
desired_caps['appActivity'] = 'com.meevii.vitacolor.HomeActivity'

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",desired_caps)
print("启动ZC成功")
driver.quit()
print("Close应用")