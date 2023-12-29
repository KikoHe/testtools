from Get_Pic import *
import PyPDF2
from PyPDF2 import errors

def test_number_error(address,limit=10):
    # 测试范围：address素材列表中今天的素材
    # 测试内容：plan和center的元素是否一致
    if address == "PBN_Story":
        storyupdatepic = Get_stroyupdatepicid()
        ids = list(storyupdatepic.keys())
        Zip_url = list(storyupdatepic.values())
    else:
        ids, Zip_url = Get_id_Zipurl(address,limit)
    failed_ids = []
    for ids_, Zip_url_ in zip(ids, Zip_url):
        data = Get_detailjson(ids_, Zip_url_, address)
        if Get_Number_From_Plan(data, address) == [] or Get_Number_From_Center(data) == []:
            failed_ids.append(ids_)
        elif set(Get_Number_From_Plan(data, address))-set(Get_Number_From_Center(data)):
            # raise ValueError(f"Plan中含有Center中没有的元素: {difference}")
            # failed_ids.insert(-1, id_)
            failed_ids.append(ids_)
    return failed_ids

def test_picupdate(address, limit=10):
    ###更新的素材张数
    if address == "PBN_Story":
        updatepic = Get_stroyupdatepicid()
        ids = list(updatepic.keys())
    else:
        ids, _ = Get_id_Zipurl(address, limit)
    print(len(ids))

def test_pdf(address, limit=10):
    ### 检查PDF文件是否能正常打开
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
