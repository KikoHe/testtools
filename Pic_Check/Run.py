import sys
from Check_Detail_Json import *
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
    # test_number_error(Project_input, Limit_input)

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
elif function_to_run == 'test_picupdate':
    if len(sys.argv) != 4:
        print("缺少必要的参数。用法: python script.py test_one_pic <Project> <PicID>")
        sys.exit(1)
    Project_input = sys.argv[2]
    PicID_input = sys.argv[3]
    try:
        test_picupdate(Project_input, PicID_input)
    except ValueError as e:
        print(e)
        sys.exit(1)
else:
    print("无效的函数。请选择 test_number_error 或 test_one_pic 作为第一个参数。")
    sys.exit(1)