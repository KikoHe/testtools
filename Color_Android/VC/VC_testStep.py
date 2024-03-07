from Common_action import *

def Open_Debug_Funtion(driver):
    click_by_id(driver, "tab_mywork")
    click_by_id(driver, "iv_setting_bg")
    long_press_until_alert(driver, "tv_ver", "custom", timeout=10)
    long_press_until_alert(driver, "tv_ver", "custom", timeout=10) ##VC客户端有BUG，要长安两次才会正常
    input_by_xpath(driver, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout\
/android.widget.FrameLayout/android.widget.FrameLayout/androidx.appcompat.widget.LinearLayoutCompat/\
android.widget.FrameLayout/android.widget.FrameLayout/android.widget.EditText", "lxdebug2018")
    click_by_id(driver, "android:id/button1")
    input_by_id(driver, "install_day", "100", timeout=30)
    time.sleep(3)
    driver.press_keycode(4)
    driver.terminate_app('com.vitastudio.color.paint.free.coloring.number')
    # driver.activate_app('com.vitastudio.color.paint.free.coloring.number')

def Fill_Pic(driver):
    element_appear_by_id(driver, "tips")
    long_press_until_alert(driver, "tips", "fill_all", timeout=10)
    click_by_id(driver, "fill_all")
    element_appear_by_id(driver, "skip")
    click_by_id(driver, "skip")

def Close_Finish(driver):
    element_appear_by_id(driver, "next")
    click_by_id(driver, "next")
    Check_Close_AD(driver)

def Close_RatausDialog(driver):
    click_by_id(driver, "close_btn", "bottom_sheet", timeout=10)

def Close_Garden_Guide(driver):
    if element_appear_by_id(driver, "garden_entrance", timeout=10):
        click_by_id(driver, "garden_entrance", timeout=10)
        time.sleep(2)
        driver.press_keycode(4)
        time.sleep(3)
        driver.press_keycode(4)
        time.sleep(3)