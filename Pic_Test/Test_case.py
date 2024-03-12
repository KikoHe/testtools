from Get_ZIP_Data import *
from Pic_Check.Common_Fun import *

def test_all_project_update_pic_date():
    test_result = []
    address_list = ["PBN_Lib", "PBN_Daily", "PBN_Story", "ZC_Lib", "ZC_Daily", "VC_Lib", "VC_Daily",\
                    "Vista_Lib", "Vista_Daily", "Vista_Pack", "BP_Lib", "BP_Daily"]
    # address_list = ["PBN_Daily", "PBN_Story", "Vista_Pack"]
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

def test_single_pic():
    PicID = ""
    Zip_url = ""
    address = "ZC"
    get_zip_detail(PicID, Zip_url, address)
    test_zip_data(address, PicID)

folder_path = '/Users/ht/Desktop/PythonTools/Pic_Test/Pic/'
delete_folder(folder_path)
# a = test_all_project_update_pic_date()
