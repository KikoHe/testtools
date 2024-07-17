import logging

from Get_zip_data import *
from Get_pic_data_from_api import *
import multiprocessing
from Common_Fun import *

# folder_path = '/Users/ht/Desktop/PythonTools/Pic_Test/Pic/'
# if os.path.exists(folder_path):
#     delete_folder(folder_path)

# 测试单张素材（SVG + PDF）
def test_single_pic(PicID, address):
    not_svg_zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(PicID, address)
    get_zip_detail(address, PicID, not_svg_zip_url)
    not_svg_test_result = test_zip_data(address, PicID)
    if svg_zip_url != '':
        get_zip_detail(address, PicID, svg_zip_url)
        svg_test_result = check_svg_by_cmd(PicID)
    else:
        svg_test_result = True
    if not_svg_test_result == False or svg_test_result == False:
        return False
    else:
        return True

# 测试单张素材（SVG）
def test_single_pic_svg(PicID, address):
    not_svg_zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(PicID, address)
    svg_test_result = True
    if svg_zip_url != '':
        get_zip_detail(address, PicID, svg_zip_url)
        svg_test_result = check_svg_by_cmd(PicID)
    return svg_test_result

# 测试明天更新的素材（通过一张一张的请求素材详情的数据,包括SVG+PDF）
def test_update_pic_single_by_single(address_input=''):
    test_result = []
    update_fail_groups = []
    if address_input == '':
        address_list = ["PBN_Lib", "PBN_Daily", "PBN_Story", "ZC_Lib", "ZC_Daily", "VC_Lib", "VC_Daily",\
                        "Vista_Lib", "Vista_Daily", "Vista_Pack", "BP_Lib", "BP_Daily"]
    else:
        address_list = [address_input]
    for address in address_list:
        logging.info("开始测试项目模块:"+str(address))
        if address == "PBN_Story":
            pid_ids = get_today_uptate_story_pic_id()
        elif address == "Vista_Pack":
            pid_ids = get_today_update_pack_pic_id()
        else:
            pid_ids, update_fail_groups = get_all_imagegroup_pic_update(address)

        fail_ids = []
        for pic_id in pid_ids:
            logging.info("开始测试素材:" + str(pic_id))
            test_zip_data_result_pdf = test_single_pic(pic_id, address)
            if test_zip_data_result_pdf == False:
                logging.error("资源测试异常的素材ID： " + str(pic_id))
                fail_ids.append(pic_id)
        update_pic_number = len(pid_ids)

        test_result_single_project = {address: [update_pic_number, fail_ids, update_fail_groups]}
        test_result.append(test_result_single_project)
    return test_result


# 通过CMS接口拉取测试素材，通过单素材接口获取测试资源（SVG+PDF）
# 要调整拉取范围，需要修改pic_config中的url即可
def test_pic_from_cms(address="PBN",offset=0,limit=100):
    id_list = pic_config(address, offset, limit)
    ids = list(id_list.keys())
    logging.info("总测试素材数" + str(len(ids)))
    fail_ids = []
    i = 1
    for PicID in ids:
        logging.info(f"第{i}个测试素材，ID： {PicID}")
        test_zip_data_result = test_single_pic(PicID, address)
        # test_zip_data_result = test_single_pic_svg(PicID, address)
        if test_zip_data_result == False:
            fail_ids.append(PicID)
            logging.error("截止目前所有异常的素材ID： " + str(fail_ids))
            output = "测试结果：" + str(PicID) + "\n"
            with open(f'output_{offset}.txt', 'a') as file:
                file.write(output)  # 写入输出结果到文件中
        i = i + 1
    return fail_ids

# 多任务同时执行
def multi_action_test():
    address = "PBN"
    offsets = [20000, 21000, 22000, 23000, 24000]
    args = [(address, offset) for offset in offsets]
    with multiprocessing.Pool() as pool:
        pool.map(test_pic_from_cms, args)

# 读取本地文件中的ID，分开输出number异常和不是number异常的素材ID
# 文件和脚本在同一个目录
def dist_error_id(filename):
    current_dir = os.getcwd()
    file = current_dir + '/' + filename
    address = "PBN"
    number_fail_ids = []
    with open(file, 'r') as f:
        content = f.read()
        content = content.strip().split('\n')
        for PicID in content:
            test_zip_data_result = test_single_pic_svg(PicID, address)
            if test_zip_data_result != None:
                number_fail_ids.append(test_zip_data_result)
        not_number_fail_ids = [x for x in content if x not in number_fail_ids]
    return number_fail_ids, not_number_fail_ids
