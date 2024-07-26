import logging

from Get_zip_data import *
from Get_pic_data_from_api import *
import multiprocessing
from Common_Fun import *

folder_path = '/Users/ht/Desktop/PythonTools/Pic_Test/Pic/'
if os.path.exists(folder_path):
    delete_folder(folder_path)

# 测试单张素材
# PicID
# address 项目
# zip_type：pdf/vector/vector/all
def test_single_pic_old(PicID, address,zip_type=''):
    pdf_zip_url, vector_zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(PicID, address)
    logging.info(f"pdf_zip_url:{pdf_zip_url}")
    logging.info(f"vector_zip_url:{vector_zip_url}")
    logging.info(f"svg_zip_url:{svg_zip_url}")

    if zip_type == "pdf": # 仅测试pdf资源
        get_zip_detail(address, PicID, pdf_zip_url)
        pdf_test_result = test_zip_data(address, PicID)
        return pdf_test_result
    if zip_type == "vector":
        get_zip_detail(address, PicID, vector_zip_url)
        vector_test_result = test_zip_data(address, PicID)
        return vector_test_result
    if zip_type == "svg" and svg_zip_url != '':
        get_zip_detail(address, PicID, svg_zip_url)
        svg_test_result = check_svg_by_cmd(PicID)
        if svg_test_result == False:
            return False
        else:
            return True
    else:  # 测试pdf和svg资源
        get_zip_detail(address, PicID, pdf_zip_url)
        pdf_test_result = test_zip_data(address, PicID)

        if svg_zip_url != '':
            get_zip_detail(address, PicID, svg_zip_url)
            svg_test_result = check_svg_by_cmd(PicID)
        else:
            svg_test_result = True
        if pdf_test_result == False or svg_test_result == False:
            return False
        else:
            return True
def test_single_pic(PicID, address, zip_type=''):
    pdf_zip_url, vector_zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(PicID, address)
    logging.info(f"pdf_zip_url:{pdf_zip_url}")
    logging.info(f"vector_zip_url:{vector_zip_url}")
    logging.info(f"svg_zip_url:{svg_zip_url}")

    def test_zip(zip_url):
        get_zip_detail(address, PicID, zip_url)
        return test_zip_data(address, PicID)

    if zip_type == "pdf":
        logging.info("仅测试pdf资源：")
        return test_zip(pdf_zip_url)

    if zip_type == "vector":
        logging.info("仅测试vector资源：")
        return test_zip(vector_zip_url)

    if zip_type == "svg" and svg_zip_url:
        logging.info("仅测试svg资源：")
        if not check_svg_by_cmd(PicID):
            return False
        return True

    logging.info("测试pdf和svg资源：")
    pdf_test_result = test_zip(pdf_zip_url)
    svg_test_result = True

    if svg_zip_url:
        svg_test_result = check_svg_by_cmd(PicID)

    return pdf_test_result and svg_test_result

# 通过客户端api获取明天更新的素材，并测试资源
def test_tomorrow_pic_from_api(address_input=''):
    test_result = []
    update_fail_groups = []
    if address_input == '':
        address_list = ["PBN_Lib", "PBN_Daily", "PBN_Story", "ZC_Lib", "ZC_Daily", "VC_Lib", "VC_Daily",\
                        "Vista_Lib", "Vista_Daily", "Vista_Pack", "BP_Lib", "BP_Daily"]
    elif isinstance(address_input, list):
        address_list = address_input
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
            test_zip_data_resul = test_single_pic(pic_id, address)
            if test_zip_data_resul == False:
                logging.error("资源测试异常的素材ID： " + str(pic_id))
                fail_ids.append(pic_id)
        update_pic_number = len(pid_ids)
        test_result_single_project = {address: [update_pic_number, fail_ids, update_fail_groups]}
        test_result.append(test_result_single_project)
    return test_result

# 通过CMS获取某天更新的素材，并测试资源
#  address_input ：项目
#  test_day：某天的运营素材
def test_releaseday_pic_from_cms(address_input='',test_day=today):
    test_result = []
    if address_input == '':
        address_list = ["PBN_Lib", "PBN_Daily", "ZC_Lib", "ZC_Daily", "VC_Lib", "VC_Daily",\
                        "Vista_Lib", "Vista_Daily", "BP_Lib", "BP_Daily"]
    else:
        address_list = [address_input]
    for address in address_list:
        logging.info("开始测试项目模块:"+str(address))
        pid_ids = get_release_day_picid_from_cms(address, test_day)
        fail_ids = []
        for pic_id in pid_ids:
            logging.info("开始测试素材:" + str(pic_id))
            test_zip_data_result = test_single_pic(pic_id, address)
            if test_zip_data_result == False:
                logging.error("资源测试异常的素材ID： " + str(pic_id))
                fail_ids.append(pic_id)
        update_pic_number = len(pid_ids)
        test_result_single_project = {address: [update_pic_number, fail_ids]}
        test_result.append(test_result_single_project)
    return test_result

# 通过CMS获取全局素材库所有素材，并进行测试
# 要调整拉取范围，需要修改pic_config中的url即可
def test_pic_from_cms(address="PBN", offset=0, limit=5000):
    id_list = get_all_picid_from_cms(address, offset, limit)
    logging.info("总测试素材数" + str(len(id_list)))
    fail_ids = []
    i = 1
    for picid in id_list:
        logging.info(f"第{i}个测试素材，ID： {picid}")
        test_zip_data_result = test_single_pic(picid, address)
        if test_zip_data_result == False:
            fail_ids.append(picid)
            logging.error("截止目前所有异常的素材ID： " + str(fail_ids))
            output = "测试结果：" + str(picid) + "\n"
            with open(f'output_{offset}.txt', 'a') as file:
                file.write(output)  # 写入输出结果到文件中
        i = i + 1
    return fail_ids

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
            test_zip_data_result = test_single_pic(PicID, address)
            if test_zip_data_result != None:
                number_fail_ids.append(test_zip_data_result)
        not_number_fail_ids = [x for x in content if x not in number_fail_ids]
    return number_fail_ids, not_number_fail_ids
