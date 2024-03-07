from Get_Pic import *
import PyPDF2,fitz
from PyPDF2 import errors
from Common_Fun import *
from Get_Pic_By_Other import *

# 检查plan和center、float center的色号、色块数据是否一致，返回不一致的素材ID
def test_number_error(address,limit=10):
    if address == "PBN_Story":
        ids,Zip_url = Get_stroyupdatepicid()
    elif address == "Vista_Pack":
        ids, Zip_url = Get_Pack_Pic_Update_Data()
    else:
        ids, Zip_url = Get_id_Zipurl(address, limit) #列表中的素材
    failed_ids = []
    for ids_, Zip_url_ in zip(ids, Zip_url):
        data = Get_detailjson(ids_, Zip_url_, address)
        if Get_Number_From_Plan(data, address) == [] or Get_Number_From_Center(data) == []:
            # 测试点：Plan或者center数据为空；表现为：整个素材不能着色
            failed_ids.append(ids_)
        elif set(Get_Number_From_Plan(data, address))-set(Get_Number_From_Center(data)):
            # 测试点：Plan和center的色快不一致；表现为：不一致的色块不能填色
            failed_ids.append(ids_)
        if Get_Number_From_FloatCenter(data) != []:
            if set(Get_Number_From_Plan(data, address))-set(Get_Number_From_FloatCenter(data)):
                # 测试点：Plan和Floatcenter的色快不一致；表现为：不一致的色块不能填色
                failed_ids.append(ids_)
        if Test_area_and_FloatCenter(data) == False:
            # 测试点：Floatcenter中的数字位置，是否在area区域内；表现为：画布上的数字不是该色块的色号数字
            failed_ids.append(ids_)
        if address.startswith("PBN") and Test_area_and_Center(data)== False:
            # 测试点：center中的数字位置，是否在area区域内；表现为：画布上的数字不是该色块的色号数字
            failed_ids.append(ids_)
    return failed_ids

# 返回更新的素材张数
def test_picupdate(address, limit=10):
    # 测试点：素材更新张数
    if address == "PBN_Story":
        ids, _ = Get_stroyupdatepicid()
        ids_output = len(ids)
    elif address == "Vista_Pack":
        ids, _ = Get_Pack_Pic_Update_Data()
        ids_output = len(ids)
    elif address in ["BP_Lib", "PBN_Lib"]:
        ids_output = Get_all_project_Lib_list_pic_ids(address, limit)
    else:
        ids, _ = Get_id_Zipurl(address, limit)
        ids_output = len(ids)
    return ids_output

# print(test_picupdate("Vista_Pack", limit=10))

# 检查PDF文件是否能正常打开,返回不能打开的素材ID
def test_pdf(address, limit=10):
    if address == "PBN_Story":
        ids, Zip_url = Get_stroyupdatepicid()
    elif address == "Vista_Pack":
        ids, Zip_url = Get_Pack_Pic_Update_Data()
    else:
        ids, Zip_url = Get_id_Zipurl(address, limit)
    failed_ids = []
    for ids_, Zip_url_ in zip(ids, Zip_url):
        pdf = Get_PDF(ids_, Zip_url_, address)
        if pdf:
            try:
                with open(pdf, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    if reader.is_encrypted:
                        continue
                    # 尝试读取PDF的每一页
                    for page in range(len(reader.pages)):
                        _ = reader.pages[page]  # 获取页面的方法也有变更
            except PyPDF2.errors.PdfReadError as e:  # 更新异常处理
                # 测试点：PDF不能正常打开；表现为：不能打开着色页
                failed_ids.append(ids_)
            except OSError as e:  # OSError 保持不变
                # 测试点：PDF不能正常打开
                failed_ids.append(ids_)
            if Check_Pdf_Block(pdf, ids_, Zip_url_, address) == False:
                # 测试点：PDF遮挡了色号数字的显示；表现后，色块被线稿遮挡，看不见
                failed_ids.append(ids_)
    return failed_ids
# print(test_pdf("Vista_Pack", limit=10))

# 获取excel表中素材ID的zip url

# print(test_pdf("VC_Daily", limit=10))

def test_error_from_excel(address):
    df = pd.read_excel('excel/12121test.xlsx', usecols=[0])
    data = df.to_dict(orient='split')
    json_data = {
        'columns': data['columns'],
        'data': data['data']
    }
    with open('excel/output.json', 'w') as f:
        json.dump(json_data, f)
    Number_failed_ids = []
    PDF_failed_ids = []
    time1 = 1
    for data in json_data["data"]:
        pic_id = data[0]
        ids_, Zip_url_ = Get_id_Zipurl_from_picdetailapi(pic_id, address)
        print(ids_)
        print(Zip_url_)
        print(time1)
        data = Get_detailjson(ids_, Zip_url_, address)
        Get_Number_From_Plan_data = Get_Number_From_Plan(data, address)
        Get_Number_From_Cente_data = Get_Number_From_Center(data)
        Get_Number_From_FloatCenter_data = Get_Number_From_FloatCenter(data)

        if Get_Number_From_Plan_data == [] or Get_Number_From_Cente_data == []:
            Number_failed_ids.append(ids_)
        elif set(Get_Number_From_Plan_data) - set(Get_Number_From_Cente_data):
            print("center:")
            print(set(Get_Number_From_Plan_data) - set(Get_Number_From_Cente_data))
            Number_failed_ids.append(ids_)

        if Get_Number_From_FloatCenter_data != []:
            if set(Get_Number_From_Plan_data)-set(Get_Number_From_FloatCenter_data):
                print("Float_center:")
                print(set(Get_Number_From_Plan_data)-set(Get_Number_From_FloatCenter_data))
                Number_failed_ids.append(ids_)
        print(Number_failed_ids)

        pdf = Get_PDF(ids_, Zip_url_, address)
        if pdf:
            try:
                with open(pdf, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    if reader.is_encrypted:
                        continue
                    for page in range(len(reader.pages)):
                        _ = reader.pages[page]  # 获取页面的方法也有变更
            except PyPDF2.errors.PdfReadError as e:  # 更新异常处理
                PDF_failed_ids.append(ids_)
            except OSError as e:  # OSError 保持不变
                PDF_failed_ids.append(ids_)
        folder_path = '/Users/ht/Desktop/PythonTools/Pic_Check/Pic/'  # 文件夹路径
        delete_folder(folder_path)
        time1 = time1 + 1
    return Number_failed_ids, PDF_failed_ids

