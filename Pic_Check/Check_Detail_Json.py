import Get_Detail, Get_PicID, Common_Fun
import sys

def test_number_equal():
    #Plan = Center
    Project = "PBN"
    limit = 1000
    ids = Get_PicID.Get_PicIDList(Project,limit)
    failed_ids = []
    for id_ in ids:
            data = Get_Detail.Get_Zip(id_, Project)
            if sorted(Get_Detail.Get_Number_From_Center(data)) != sorted(Get_Detail.Get_Number_From_Plan(data)):
                failed_ids.insert(-1, id_)
            continue

def test_number_error(Project,limit=10):
    # Plan > Center
    ids = Get_PicID.Get_PicIDList(Project,limit)
    print(len(ids))
    failed_ids = []
    for id_ in ids:
        data = Get_Detail.Get_Zip(id_, Project)
        difference = set(Get_Detail.Get_Number_From_Plan(data))-set(Get_Detail.Get_Number_From_Center(data))
        if difference:
            # raise ValueError(f"Plan中含有Center中没有的元素: {difference}")
            # failed_ids.insert(-1, id_)
            failed_ids.append(id_)
        else:
            Common_Fun.remove_zip_files_and_directories(id_)
    return failed_ids

def test_one_pic(Project, PicID):
    data = Get_Detail.Get_Zip(PicID, Project)
    difference = set(Get_Detail.Get_Number_From_Plan(data)) - set(Get_Detail.Get_Number_From_Center(data))
    if difference:
        raise ValueError(f"Plan中含有Center中没有的元素: {difference}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python script.py <function> [<Project>] [<PicID> | <Limit>]")
        sys.exit(1)

    function_to_run = sys.argv[1]

    if function_to_run == 'test_number_error':
        if len(sys.argv) != 4:
            print("缺少必要的参数。用法: python script.py test_number_error <Project> <Limit>")
            sys.exit(1)
        Project_input = sys.argv[2]
        Limit_input = int(sys.argv[3])
        print(test_number_error(Project_input, Limit_input))

    elif function_to_run == 'test_one_pic':
        if len(sys.argv) != 4:
            print("缺少必要的参数。用法: python script.py test_one_pic <Project> <PicID>")
            sys.exit(1)
        Project_input = sys.argv[2]
        PicID_input = sys.argv[3]
        try:
            test_one_pic(Project_input, PicID_input)
        except ValueError as e:
            print(e)
            sys.exit(1)

    else:
        print("无效的函数。请选择 test_number_error 或 test_one_pic 作为第一个参数。")
        sys.exit(1)
