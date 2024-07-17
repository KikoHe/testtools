import logging

from Public_env import *
from PyPDF2 import errors
from Get_pic_data import *
from Get_pic_data_from_api import *
from Common_Fun import *

# 然后获取素材detailjson内的数据
def get_data_from_zip(address,pic_id):
    if address.startswith("BP"):
        datajson = home + "/" + str(pic_id) + "/" + "data.json"
        pdf = os.path.join(home, str(pic_id), "origin.pdf")
    else:
        datajson = home + "/" + str(pic_id) + "/" + "detail.json"
        pic_region_path = os.path.join(home, str(pic_id), f"{pic_id}_origin")
        pdf = f"{pic_region_path}.pdf"
        if os.path.exists(pic_region_path) and os.path.isfile(pic_region_path):
            os.rename(pic_region_path, pdf)
        else:
            logging.warning("不存在pdf资源： "+str(pic_region_path))
            pass

    with open(datajson, "r") as file:
        detail_json_data = json.load(file)
    return detail_json_data, pdf

def get_single_data_from_detail_json(address, detail_json_data, data_type):
    if data_type == "plans" and address.startswith("BP"):
        data_type = "color"

    if data_type in detail_json_data:
        data = detail_json_data[data_type]
        if data is not None:
            return data
        else:
            logging.warning("这个key的value为空： " + str(data_type))
            return False
    else:
        logging.warning("没有这个key： "+str(data_type))
        return False

def get_all_data_and_pdf(address,pic_id):
    detail_json_data, pdf = get_data_from_zip(address,pic_id)

    center_data = get_single_data_from_detail_json(address, detail_json_data, "center")
    if center_data == False:
        center_data_block_list = []
        center_data_block_number_list = []
    else:
        center_data_block_list = center_data.split('|')
        center_data_block_number_list = []
        for center_data_block_number in center_data_block_list:
            center_data_block_number_list.append(center_data_block_number.split(',')[0])

    center_float_data = get_single_data_from_detail_json(address, detail_json_data, "center_float")
    if center_float_data == False:
        center_float_data_block_list = []
        center_float_data_block_number_list = []
    else:
        center_float_data_block_list = center_float_data.split('|')
        center_float_data_block_number_list = []
        for center_float_data_block_number in center_float_data_block_list:
            center_float_data_block_number_list.append(center_float_data_block_number.split(',')[0])

    plans_data = get_single_data_from_detail_json(address, detail_json_data, "plans")
    if plans_data == False:
        plans_data_block_list = []
        plans_data_block_group_list = []
    else:
        plans_data_block_group_list = plans_data[0].split('|')
        plans_data_block_list = []
        block_group_number = 1
        for block_group_data in plans_data_block_group_list:
            block_group = block_group_data.split('#')[0].split(',')
            for block in block_group:
                plans_data_block_list.append(block)
                if block == "96":
                    logging.info("你要找的色块对应的色号是： "+str(block_group_number))
            block_group_number = block_group_number + 1

    area_data = get_single_data_from_detail_json(address, detail_json_data, "area")
    if area_data == False:
        area_data_block_number_list = []
    else:
        area_data_block_number_list = list(area_data.keys())

    return center_data_block_number_list, center_data_block_list,\
           center_float_data_block_number_list, center_float_data_block_list,\
           plans_data_block_list, area_data_block_number_list, area_data, pdf

# 检测非SVG资源
def test_zip_data(address, pic_id):
    center_number, center_data, centerfloat_number, centerfloat_data,\
    plans_number, area_number, area_data, pdf = get_all_data_and_pdf(address, pic_id)

    # 检查资源是否为空
    if plans_number == []:
        logging.error("plans_number 为空")
        return False
    if address.startswith(("VC", "ZC", "Vista")) and centerfloat_number == []:
        logging.error("centerfloat_number 为空")
        return False
    if address.startswith(("PBN", "BP")) and center_number == []:
        logging.error("center_number 为空")
        return False
    if area_number == []:
        logging.warning("【警告】area_number 为空，但不会报错")  # area资源完全为空的时候，客户端会重新计算，所以不返回flase
        # area_number, area_data = get_area_from_vincent(pic_id)
        pass

    ### 检查floatcenter的色块是否比plan少，如果floatcenter缺少了，则不能定位，且没有色号显示在色块上，除了PBN，都用的floatcenter资源
    if address.startswith(("VC", "ZC", "Vista", "PBN")):
        set_plans_number = set(plans_number)
        set_centerfloat_number = set(centerfloat_number)
        centerfloat_number_more = set_centerfloat_number.difference(set_plans_number)
        if centerfloat_number_more and centerfloat_number != []:
            logging.warning("【警告】centerfloat比plan多的色块： "+str(centerfloat_number_more))
            pass
        plans_number_more = set_plans_number.difference(set_centerfloat_number)
        if plans_number_more and centerfloat_number != []:
            logging.error("centerfloat比plan少的色块： " + str(plans_number_more))
            return False

    ### 检查center的色块是否比plan少，如果center缺少了，则不能定位，且没有色号显示在色块上，只检查PBN，是因为暂时只有PBN用center资源
    if address.startswith(("PBN", "BP")):
        set_plans_number = set(plans_number)
        set_center_number = set(center_number)
        center_number_more = set_center_number.difference(set_plans_number)
        if center_number_more:
            logging.warning("【警告】center比plan多的色块： "+str(center_number_more))    # centerfloat多了色块，不会对着色流程造成影响，就不返回Flase了
            pass
        plans_number_more = set_plans_number.difference(set_center_number)
        if plans_number_more:
            logging.error("center比plan少的色块： "+str(plans_number_more))
            return False

    ### 检查area的色块是否比plan中的少，如果少了，Android客户端这个色块就不能填色，不检查vista是因为iOS会自己生成这个资源
    if address.startswith(("VC", "ZC", "BP", "PBN")) and area_number != []:
        set_plans_number = set(plans_number)
        set_area_number = set(area_number)
        plans_number_more = set_plans_number.difference(set_area_number)
        if plans_number_more:
            logging.error("area中缺少的色块： " + str(plans_number_more))
            return False
        area_numberr_more = set_area_number.difference(set_plans_number)
        if area_numberr_more:
            logging.warning("【警告】area中多的色块： " + str(area_numberr_more))   # area的色块比plan多的情况，客户端不会报错，就不返回False了
            pass

    ### 检查floatcenter中的x,y坐标一定是落在area的色块矩形区域内，通过这个方法能检查出色号显示错乱的问题，比如色号1的色块显示的色号是5,PBN用的是center，而不是floatcenter
    if address.startswith(("PBN", "VC", "ZC")):
        for center_data_block in centerfloat_data:
            center_data_block_detail = center_data_block.split(',')
            center_data_block_detail_number = center_data_block_detail[0]
            center_data_block_detail_x = float(center_data_block_detail[1])
            center_data_block_detail_y = float(center_data_block_detail[2])
            center_data_block_detail_r = float(center_data_block_detail[3])

            if center_data_block_detail_number in area_number:
                area_data_block_detail = area_data[center_data_block_detail_number]
                x_min = area_data_block_detail["minX"]
                x_max = area_data_block_detail["maxX"]
                y_min = area_data_block_detail["minY"]
                y_max = area_data_block_detail["maxY"]
                if x_min-center_data_block_detail_r < center_data_block_detail_x < x_max+center_data_block_detail_r\
                        and y_min-center_data_block_detail_r < center_data_block_detail_y < y_max+center_data_block_detail_r:
                    pass
                else:
                    logging.warning("【警告】色号上的数据显示的位置是错误的/偏移的："+str(center_data_block_detail_number))
                    pass

    ### 检查center中的x,y坐标一定是落在area的色块矩形区域内，通过这个方法能检查出色号显示错乱的问题，比如色号1的色块显示的色号是5,PBN 用的是center，而是floatcenter
    if address.startswith(("PBN", "BP")):
        for center_data_block in center_data:
            center_data_block_detail = center_data_block.split(',')
            center_data_block_detail_number = center_data_block_detail[0]
            center_data_block_detail_x = float(center_data_block_detail[1])
            center_data_block_detail_y = float(center_data_block_detail[2])
            center_data_block_detail_r = float(center_data_block_detail[3])

            if center_data_block_detail_number in area_number:
                area_data_block_detail = area_data[center_data_block_detail_number]
                x_min = area_data_block_detail["minX"]
                x_max = area_data_block_detail["maxX"]
                y_min = area_data_block_detail["minY"]
                y_max = area_data_block_detail["maxY"]
                if x_min-center_data_block_detail_r < center_data_block_detail_x < x_max+center_data_block_detail_r\
                        and y_min-center_data_block_detail_r < center_data_block_detail_y < y_max+center_data_block_detail_r:
                    pass
                else:
                    logging.warning("【警告】色号上的数据显示的位置是错误的/偏移的："+str(center_data_block_detail_number))
                    pass

    if os.path.isfile(pdf):
        ### 检查pdf资源是否被破坏，是否能正常打开
        try:
            with open(pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if reader.is_encrypted == False:
                    for page in range(len(reader.pages)):
                        _ = reader.pages[page]
        except PyPDF2.errors.PdfReadError as e:  # 更新异常处理
            logging.error("不能打开这个PDF资源，具体原因： "+str(e))
            return False
        except OSError as e:  # OSError 保持不变
            logging.error("不能打开这个PDF资源，具体原因： "+str(e))
            return False

        ### 检查色块上的数字是否和PDF线稿有重叠，同时能判断色块不可见的问题
        doc = fitz.open(pdf)
        page = doc[0]
        for axis in centerfloat_data:
            axis_detail = axis.split(',')
            number, x, y, r = axis_detail[0], axis_detail[1], axis_detail[2], axis_detail[3]
            if number in plans_number:
                x1, y1 = float(x) - float(r), float(y) - float(r)
                x2, y2 = float(x) + float(r), float(y) + float(r)
                bbox = fitz.Rect(x1, y1, x2, y2)
                if float(r) < 5:   # 仅测试小色块，阈值为5
                    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), clip=bbox)
                    pixel_value = int.from_bytes(pix.samples, byteorder='big')
                    if pixel_value < 255:    # 小于255，则不透明，有重叠
                        logging.warning("【警告】这个色块和pdf资源有重叠风险： "+str(number))
                        pass
    return True
# 通过工具检查SVG资源
def check_svg_by_cmd(picid):
    tool_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = home + f"/{picid}"
    try:
        command = [f'{tool_dir}/LXSVGValidate', filename]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return True
        else:
            # 打印标准输出和标准错误
            logging.error(stdout)
            return False
    except subprocess.CalledProcessError as e:
        logging.error("Test Fail: %s", e)
        return False