from Get_Pic import *
import PyPDF2
from PyPDF2 import errors
# from Common_Fun import *

# 测试范围：address素材列表中今天的素材
# 测试内容：plan和center的元素是否一致
# 测试内容：plan和float center的元素是否一致
def test_number_error(address,limit=10):
    if address == "PBN_Story":
        storyupdatepic = Get_stroyupdatepicid()
        ids = list(storyupdatepic.keys())
        Zip_url = list(storyupdatepic.values())
    else:
        ids, Zip_url = Get_id_Zipurl(address,limit) #列表中的素材
    failed_ids = []
    for ids_, Zip_url_ in zip(ids, Zip_url):
        data = Get_detailjson(ids_, Zip_url_, address)
        if Get_Number_From_Plan(data, address) == [] or Get_Number_From_Center(data) == []:
            failed_ids.append(ids_)
        elif set(Get_Number_From_Plan(data, address))-set(Get_Number_From_Center(data)):
            failed_ids.append(ids_)
        if Get_Number_From_FloatCenter(data) != []:
            if set(Get_Number_From_Plan(data, address))-set(Get_Number_From_FloatCenter(data)):
                failed_ids.append(ids_)
    return failed_ids

print(test_number_error("PBN_Lib",limit=30))

# 返回更新的素材张数

def test_picupdate(address, limit=10):
    if address == "PBN_Story":
        updatepic = Get_stroyupdatepicid()
        ids = list(updatepic.keys())
        ids_output = len(ids)
    elif address in ["BP_Lib", "PBN_Lib"]:
        ids_output = Get_all_project_Lib_list_pic_ids(address,limit)
    else:
        ids, _ = Get_id_Zipurl(address, limit)
        ids_output = len(ids)
    return ids_output

# 检查PDF文件是否能正常打开
def test_pdf(address, limit=10):
    if address == "PBN_Story":
        storyupdatepic = Get_stroyupdatepicid()
        ids = list(storyupdatepic.keys())
        Zip_url = list(storyupdatepic.values())
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
                        # print(f"文件 {pdf} 已加密。")
                        continue
                    # 尝试读取PDF的每一页
                    for page in range(len(reader.pages)):
                        _ = reader.pages[page]  # 获取页面的方法也有变更
                    # success_ids.append(ids_)  ##测试代码
            except PyPDF2.errors.PdfReadError as e:  # 更新异常处理
                failed_ids.append(ids_)
            except OSError as e:  # OSError 保持不变
                failed_ids.append(ids_)
    return failed_ids

# 获取excel表中素材ID的zip url
# def test_error_from_excel(address):
#     df = pd.read_excel('excel/12121test.xlsx', usecols=[0])
#     data = df.to_dict(orient='split')
#     json_data = {
#         'columns': data['columns'],
#         'data': data['data']
#     }
#     with open('excel/output.json', 'w') as f:
#         json.dump(json_data, f)
#     Number_failed_ids = []
#     PDF_failed_ids = []
#     time1 = 1
#     for data in json_data["data"]:
#         pic_id = data[0]
#         ids_, Zip_url_ = Get_id_Zipurl_from_picdetailapi(pic_id, address)
#         print(ids_)
#         print(Zip_url_)
#         print(time1)
#         data = Get_detailjson(ids_, Zip_url_, address)
#         Get_Number_From_Plan_data = Get_Number_From_Plan(data, address)
#         Get_Number_From_Cente_data = Get_Number_From_Center(data)
#         Get_Number_From_FloatCenter_data = Get_Number_From_FloatCenter(data)
#
#         if Get_Number_From_Plan_data == [] or Get_Number_From_Cente_data == []:
#             Number_failed_ids.append(ids_)
#         elif set(Get_Number_From_Plan_data) - set(Get_Number_From_Cente_data):
#             print("center:")
#             print(set(Get_Number_From_Plan_data) - set(Get_Number_From_Cente_data))
#             Number_failed_ids.append(ids_)
#
#         if Get_Number_From_FloatCenter_data != []:
#             if set(Get_Number_From_Plan_data)-set(Get_Number_From_FloatCenter_data):
#                 print("Float_center:")
#                 print(set(Get_Number_From_Plan_data)-set(Get_Number_From_FloatCenter_data))
#                 Number_failed_ids.append(ids_)
#         print(Number_failed_ids)
#
#         pdf = Get_PDF(ids_, Zip_url_, address)
#         if pdf:
#             try:
#                 with open(pdf, 'rb') as file:
#                     reader = PyPDF2.PdfReader(file)
#                     if reader.is_encrypted:
#                         continue
#                     for page in range(len(reader.pages)):
#                         _ = reader.pages[page]  # 获取页面的方法也有变更
#             except PyPDF2.errors.PdfReadError as e:  # 更新异常处理
#                 PDF_failed_ids.append(ids_)
#             except OSError as e:  # OSError 保持不变
#                 PDF_failed_ids.append(ids_)
#         delete_folder()
#         time1 = time1 + 1
#     return Number_failed_ids, PDF_failed_ids