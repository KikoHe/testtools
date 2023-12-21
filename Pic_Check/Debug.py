from Get_Pic import *
from Common_Fun import *

def test_number_error():
    #Plan = Center
    Project = "PBN"
    limit = 1000
    ids = Get_Picid(Project,limit)
    failed_ids = []
    for id_ in ids:
            data = Get_Zip(id_, Project)
            if sorted(Get_Number_From_Center(data)) != sorted(Get_Number_From_Plan(data)):
                failed_ids.insert(-1, id_)
            continue


def test_one_pic(address, PicID):
    # 测试范围：PicID
    # 测试内容：plan和center的元素是否一致
    data = Get_detailjson(PicID, address)
    difference = set(Get_Number_From_Plan(data)) - set(Get_Number_From_Center(data))
    if difference:
        raise ValueError(f"Plan中含有Center中没有的元素: {difference}")