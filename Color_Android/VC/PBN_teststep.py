from Common_action import *
def test(driver):
    click_by_id(driver, "paint.by.number.pixel.art.coloring.drawing.puzzle:id/tv_desc")
    click_by_id(driver, "paint.by.number.pixel.art.coloring.drawing.puzzle:id/tab_mine")
    click_by_id(driver, "paint.by.number.pixel.art.coloring.drawing.puzzle:id/iv_setting")
    time.sleep(5)
    status = get_elements_attribute_by_id(driver, "paint.by.number.pixel.art.coloring.drawing.puzzle:id/switch_btn","checked", index=3, timeout=10)
    return status