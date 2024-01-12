from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import os, shutil, time
from datetime import datetime

def click_by_id(driver, element_id_click:str, element_id_check:str = None, index=0 , timeout=30):
    ###通过ID的方式，点击某个元素
    ###多加了一个检查元素element_id_check
    id_full_click = Get_id(element_id_click)
    if element_id_check is None:
        id_full_check = id_full_click
    else:
        id_full_check = Get_id(element_id_check)

    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, id_full_check)))
        elements = driver.find_elements(By.ID, id_full_click)
        elements[index].click()
        print("点击：" + id_full_click)
    except TimeoutException:
        print(f"等待超过30秒后元素未出现。" + id_full_check)

def element_disappear_by_id(driver, element_id, timeout=10):
    ###通过ID方式等到某个元素消失
    element_id = Get_id(element_id)
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((By.ID, element_id)))
        print("元素消失" + element_id)
    except TimeoutException:
        print("元素还在" + element_id)

def element_appear_by_id(driver, element_id, timeout=10):
    ###通过ID方式等到某个元素出现
    element_id = Get_id(element_id)
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, element_id)))
        print("元素出现：" + element_id)
    except TimeoutException:
        print("元素消失：" + element_id)

def element_appear_by_xpath(driver, element_xpath, timeout=10):
    ###通过Xpath方式等到某个元素出现
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        print("元素出现：" + element_xpath)
    except TimeoutException:
        print("元素消失：" + element_xpath)

def Get_id(id_simple):
    ###给ID添加包前缀
    if "/" not in id_simple:
        id_full = f"com.vitastudio.color.paint.free.coloring.number:id/{id_simple}"
    else:
        id_full = id_simple
    return id_full

def long_press_until_alert(driver, element_id, alert_id, timeout=10):
    ###长按某个元素，直到另外一个元素出现
    ###通过过ID的方式
    # 找到要长按的元素
    element_id = Get_id(element_id)
    alert_id = Get_id(alert_id)
    element_to_long_press = driver.find_element(By.ID, element_id)

    # 创建 TouchAction 实例进行长按操作
    touch_action = TouchAction(driver)
    touch_action.long_press(element_to_long_press).perform()

    # 等待弹窗元素出现
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, alert_id)))
        print("弹窗已出现。")
    except TimeoutException:
        print("在指定时间内未检测到弹窗。")

def input_by_xpath(driver, element_xpath, text, timeout=30):
    ###通过Xpath方式找到某个输入框，并输入内容
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        input_element = driver.find_element(By.XPATH, element_xpath)
        input_element.send_keys(text)
        print("输入：" + text)
    except TimeoutException:
        print(f"等待超过30秒后元素未出现。" + element_xpath)

def input_by_id(driver, element_id, text, timeout=30):
    ###通过Xpath方式找到某个输入框，并输入内容
    element_id = Get_id(element_id)
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, element_id)))
        input_element = driver.find_element(By.ID, element_id)
        input_element.send_keys(text)
        print("输入：" + text)
    except TimeoutException:
        print(f"等待超过30秒后元素未出现。" + element_id)

def swipe(driver, action):
    ###向上/下滑动屏幕
    # 获取屏幕的大小
    size = driver.get_window_size()

    # 计算滑动的起始点和结束点
    start_x = size['width'] / 2
    start_y = size['height'] * 0.2
    end_x = start_x
    end_y = size['height'] * 0.8

    # 执行滑动
    if action == "upper":
        TouchAction(driver).press(x=start_x, y=start_y).wait(ms=1000).move_to(x=end_x, y=end_y).release().perform() #向上滑动
    elif action == "down":
        TouchAction(driver).press(x=end_x, y=end_y).wait(ms=1000).move_to(x=start_x, y=start_y).release().perform() #向下滑动
    else:
        print("参数应该是upper/down，输入错误：" + action)


def click_back_until_element_disappears(driver, element_id, timeout=60, interval=5):
    ###Delete
    end_time = time.time() + timeout
    element_id = Get_id(element_id)
    while True:
        # 检查元素是否存在
        try:
            # 这里设置WebDriverWait的超时时间为很短，因为我们只是想知道元素是否还在，而不需要等太久
            WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, element_id)))
        except TimeoutException:
            # 如果等待过程中抛出TimeoutException异常，则认为元素已经不再出现，退出函数
            print("元素已经消失")
            break

        # 点击物理返回键
        driver.press_keycode(4)
        print("点击了物理返回键")

        # 检查是否超时
        if time.time() > end_time:
            print("超过指定的超时时间，停止点击")
            break

        # 等待指定的时间间隔
        time.sleep(interval)   ###wuyong

def get_element_attribute_by_id(driver, element_id, attribute, timeout=10):
    ###通过ID方式找到某个元素，并返回这个元素的某个属性
    try:
        # 等待直到父元素可见
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        element_attribute = driver.find_element(By.ID, element_id).get_attribute(attribute)
        print(f"Enabled status: {element_id}")
        return element_attribute
    except TimeoutException:
        print(f"No element found with ID: {element_id}")

def is_element_has_children_by_xpath(driver, parent_xpath, wait_time=10):
    ###通过xpath检查某个元素是否有子路径
    try:
        # 等待直到父元素可见
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, parent_xpath))
        )
        children_xpath = parent_xpath + "/*"
        WebDriverWait(driver, wait_time).until(
            EC.visibility_of_element_located((By.XPATH, children_xpath))
        )
        print("Banner AD Show~")
    except TimeoutException:
        print("Not Banner AD Show~")

def check_element_id_by_xpath(driver, element_xpath, expected_id, timeout=10):
    ###通过xpath找到某个元素，如果该元素的ID和预期一致，则返回ture，否则返回false
    try:
        # 定位到元素
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, element_xpath))
        )
        element = driver.find_element(By.XPATH, element_xpath)
        # 获取元素的ID属性
        if element.get_attribute("resource-id"):
            actual_id = element.get_attribute("resource-id")
        # 判断实际的ID是否与预期相符
            if actual_id == expected_id:
                print("通过ID和xpath路径判断是广告页面")
                return True
            else:
                print("Element found, but 'resource-id' does not match the expected value.")
                return False
        else:
            print("Element found, but it does not have a 'resource-id' attribute.")
            return False
    except TimeoutException:
        # 如果等待超时，则意味着元素没有在指定时间内变得可见
        print(f"Timeout waiting for element with XPath: {element_xpath}")
        return False
    except NoSuchElementException:
        # 如果找不到元素，则返回False
        print(f"No element found with XPath: {element_xpath}")
        return False

def find_all_new_pic(driver, element_id):
    ###通过ID的方式找到全部元素，并以list返回
    element_id = Get_id(element_id)
    try:
        # 直接使用ID字符串查找元素
        elements = driver.find_elements(By.ID, element_id)
        if not elements:
            print(f"没有找到ID为 '{element_id}' 的元素。")
        else:
            print(f"所有ID为 '{element_id}' 的元素都是可见的。")
        return elements
    except NoSuchElementException:
        print(f"页面上不存在ID为 '{element_id}' 的元素。")

def Check_Close_AD(driver):
    ###有全屏广告时并截图保存
    if check_element_id_by_xpath(driver, "hierarchy/android.widget.FrameLayout/\
android.widget.LinearLayout/android.widget.FrameLayout", "android:id/content"):
        take_screenshot_and_save(driver, save_path="/screenshots", file_name="FullScreen_AD")
    ###关闭全屏广告
    while check_element_id_by_xpath(driver, "hierarchy/android.widget.FrameLayout/\
android.widget.LinearLayout/android.widget.FrameLayout", "android:id/content"):
        driver.press_keycode(4)
        click_byid(driver, "m-playable-skip", timeout=1)
        # 等待指定的时间间隔
        time.sleep(5)
        if check_element_id_by_xpath(driver, "hierarchy/android.widget.FrameLayout/\
android.widget.LinearLayout/android.widget.FrameLayout", "android:id/content") == False:
            print("AD 消失")
            break

def remove_directory(dir_path):
    ###删除当前文件所处目录下的某个路径
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    dir_path = current_dir + dir_path
    # 首先检查该路径是否确实存在，并且是一个目录
    if os.path.isdir(dir_path):
        # 使用shutil.rmtree来递归删除目录
        shutil.rmtree(dir_path)
        print(f"The directory {dir_path} has been removed.")
    else:
        print(f"The path {dir_path} does not exist or is not a directory.")

def take_screenshot_and_save(driver, save_path="/screenshots", file_name="screenshots"):
    ###截图并保存到当前目录下的某个路径下
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    save_path = current_dir+save_path
    # 确保保存截图的路径存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # 获取当前时间戳作为文件名的一部分
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    full_file_name = f"{file_name}_{timestamp}.png"
    file_path = os.path.join(save_path, full_file_name)

    # 如果该文件名已存在，则增加一个后缀直到找到未使用的文件名
    file_index = 1
    while os.path.isfile(file_path):
        file_path = os.path.join(save_path, f"{file_name}_{timestamp}_{file_index}.png")
        file_index += 1

    # 截图并获取图片数据
    screenshot_data = driver.get_screenshot_as_png()

    # 将截图数据写入文件
    with open(file_path, "wb") as file:
        file.write(screenshot_data)

    print(f"Screenshot taken and saved to {file_path}")