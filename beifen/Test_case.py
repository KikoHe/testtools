from Get_zip_data import *
from Pic_Check.Common_Fun import *
from Get_pic_data_from_api import *
import multiprocessing
from functools import partial
import time

# 测试单张的素材
def test_single_pic(PicID, address):
    not_svg_zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(PicID, address)
    get_zip_detail(address, PicID, not_svg_zip_url)
    not_svg_test_result = test_zip_data(address, PicID)
    if svg_zip_url != '':
        get_zip_detail(address, PicID, svg_zip_url)
        svg_test_result = check_svg_by_cmd(PicID)
    else:
        print("没有SVG资源！！！")
        svg_test_result = True
    if not_svg_test_result == False or svg_test_result == False:
        return False
    else:
        return True

# 测试单张的素材SVG资源
def test_single_pic_svg(PicID, address):
    Zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(address, PicID)
    result = []
    if svg_zip_url != []:
        svg_zip_url = svg_zip_url[0]
        get_zip_detail(address, PicID, svg_zip_url)
        result = check_svg_by_cmd(PicID)
    return result

# 测试明天更新的素材
def test_all_project_update_pic_date():
    test_result = []
    address_list = ["PBN_Lib", "PBN_Daily", "PBN_Story", "ZC_Lib", "ZC_Daily", "VC_Lib", "VC_Daily",\
                    "Vista_Lib", "Vista_Daily", "Vista_Pack", "BP_Lib", "BP_Daily"]
    address_list = ["PBN_Lib"]
    for address in address_list:
        print("开始测试项目模块： "+str(address))
        if address == "PBN_Story":
            update_pic_data = get_today_uptate_story_pic_data()
        elif address == "Vista_Pack":
            update_pic_data = get_today_update_pack_pic_data()
        else:
            update_pic_data = get_all_imagegroup_pic_update(address)
        fail_ids = []
        if isinstance(update_pic_data, dict):
            for pic_id, zip_url in update_pic_data.items():
                print("开始测试素材： " + str(pic_id))
                get_zip_detail(address, pic_id, zip_url)
                test_zip_data_result = test_zip_data(address, pic_id)
                if test_zip_data_result == False:
                    print("资源测试异常的素材ID： " + str(pic_id))
                    fail_ids.append(pic_id)
            value1 = len(update_pic_data)
        else:
            value1 = update_pic_data
        test_result_single_project = {address: [value1, fail_ids]}
        test_result.append(test_result_single_project)
    print("最终测试结果："+str(test_result))

# 通过一张一张的请求素材详情的数据，测试明天更新的素材,包括SVG资源
def test_update_pic_single_by_single():
    test_result = []
    address_list = ["PBN_Lib", "PBN_Daily", "PBN_Story", "ZC_Lib", "ZC_Daily", "VC_Lib", "VC_Daily",\
                    "Vista_Lib", "Vista_Daily", "Vista_Pack", "BP_Lib", "BP_Daily"]
    for address in address_list:
        print("开始测试项目模块:"+str(address))
        if address == "PBN_Story":
            update_pic_data = get_today_uptate_story_pic_data()
        elif address == "Vista_Pack":
            update_pic_data = get_today_update_pack_pic_data()
        else:
            update_pic_data = get_all_imagegroup_pic_update(address)
        fail_ids = []
        if isinstance(update_pic_data, dict):
            for pic_id, zip_url in update_pic_data.items():
                print("开始测试素材:" + str(pic_id))
                test_zip_data_result_pdf = test_single_pic(pic_id, address)
                if test_zip_data_result_pdf == False:
                    print("资源测试异常的素材ID： " + str(pic_id))
                    fail_ids.append(pic_id)
            value1 = len(update_pic_data)
        else:
            value1 = update_pic_data
        test_result_single_project = {address: [value1, fail_ids]}
        test_result.append(test_result_single_project)
    print("最终测试结果：" + str(test_result))
test_update_pic_single_by_single()



# 测试CMS上拉取的素材，要调整拉取范围，需要修改pic_config中的url即可
def test_pic_svg_from_cms(address,offset):
    id_list = pic_config(address,offset)
    ids = list(id_list.keys())
    print("总测试素材数" + str(len(ids)))
    fail_ids = []
    i = 1
    for PicID in ids:
        print(f"第{i}个测试素材，ID： {PicID}")
        test_zip_data_result = test_single_pic_svg(PicID, address)
        if test_zip_data_result != None:
            fail_ids.append(test_zip_data_result)
            print("所有异常的素材ID： " + str(fail_ids))
        i = i + 1
    return fail_ids

# 测试CMS上拉取的素材，要调整拉取范围，需要修改pic_config中的url即可
def test_pic_from_cms(address,offset):
    id_list = pic_config(address,offset)
    ids = list(id_list.keys())
    print("总测试素材数" + str(len(ids)))
    fail_ids = []
    i = 1
    for PicID in ids:
        print(f"第{i}个测试素材，ID： {PicID}")
        test_zip_data_result = test_single_pic(PicID, address)
        if test_zip_data_result == False:
            fail_ids.append(PicID)
            print("所有异常的素材ID： " + str(fail_ids))
        i = i + 1
    return fail_ids

folder_path = '/Users/ht/Desktop/PythonTools/Pic_Test/Pic/'
delete_folder(folder_path)

# 测试单张素材
# address = "PBN"
# PicID = "66138da4167c11dcc3593b0f"
# a = test_single_pic_svg(PicID, address)

# 测试CMS全部素材
# pro = ["PBN", "ZC", "VC", "Vista"]
def task(offset):
    a = test_pic_svg_from_cms("PBN", offset)
    output = "测试结果：" + str(a) + "\n"
    with open(f'output_{offset}.txt', 'w') as file:
        file.write(output)  # 写入输出结果到文件中

def task1():
    current_dir = os.getcwd()
    file = current_dir + '/merged_output.txt'
    address = "PBN"
    number_fail_ids = []
    with open(file, 'r') as f:
        content = f.read()
        content = content.strip().split('\n')
        print(content)
        for PicID in content:
            test_zip_data_result = test_single_pic_svg(PicID, address)
            if test_zip_data_result != None:
                number_fail_ids.append(test_zip_data_result)
                print("number_fail_ids:" + str(number_fail_ids))
        not_number_fail_ids = [x for x in content if x not in number_fail_ids]
        print("not_number_fail_ids:" + str(not_number_fail_ids))
# task1()


# 多任务同时执行
# if __name__ == "__main__":
#     with multiprocessing.Pool() as pool:
#         pool.map(task, (20000, 21000, 22000, 23000, 24000))


