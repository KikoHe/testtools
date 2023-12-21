from Get_Pic import *
from Common_Fun import *
import PyPDF2
from PyPDF2 import errors

def test_number_error(address,limit=10):
    # 测试范围：address素材列表中今天的素材
    # 测试内容：plan和center的元素是否一致
    ids = Get_Picid(address,limit)
    failed_ids = []
    for id_ in ids:
        data = Get_detailjson(id_, address)
        difference = set(Get_Number_From_Plan(data))-set(Get_Number_From_Center(data))
        if difference:
            # raise ValueError(f"Plan中含有Center中没有的元素: {difference}")
            # failed_ids.insert(-1, id_)
            failed_ids.append(id_)
        else:
            remove_zip_files_and_directories(id_)
    return failed_ids

def test_picupdate(address,limit):
    ids = Get_Picid(address,limit)
    print(len(ids))

def test_pdf(address,limit):
    ### 检查PDF文件
    ids = Get_Picid(address, limit)
    failed_ids = []
    for id_ in ids:
        pdf = Get_PDF(id_, address)
        if pdf:
            try:
                with open(pdf, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    if reader.is_encrypted:
                        print(f"文件 {pdf} 已加密。")
                        continue
                    # 尝试读取PDF的每一页
                    for page in range(len(reader.pages)):
                        _ = reader.pages[page]  # 获取页面的方法也有变更
                    print(f"文件 {pdf} 可以正常打开。")
            except PyPDF2.errors.PdfReadError as e:  # 更新异常处理
                print(f"无法打开文件 {pdf}: {e}")
            except OSError as e:  # OSError 保持不变
                print(f"操作系统错误 {pdf}: {e}")
                failed_ids.append(id_)
        else:
            print("没有PDF资源")