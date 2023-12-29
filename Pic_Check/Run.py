import sys
from Check_Detail_Json import *
import shutil
import os

# 参数检查和解析函数
def parse_args(expected_length, usage_message):
    if len(sys.argv) != expected_length:
        print(usage_message)
        sys.exit(1)
    return sys.argv[2], sys.argv[3]


# 函数映射字典
function_mappings = {
    'test_number_error': (test_number_error, "用法: python script.py test_number_error <Project> <Limit>"),
    'test_picupdate': (test_picupdate, "用法: python script.py test_picupdate <Project> <Limit>"),
    'test_pdf': (test_pdf, "用法: python script.py test_pdf <Project> <Limit>")
}


def main():
    # 检查最基本的参数长度
    if len(sys.argv) < 2:
        print("用法: python script.py <function> [<Project>] [<PicID> | <Limit>]")
        sys.exit(1)

    # 获取要运行的函数名称
    function_to_run = sys.argv[1]

    # 根据函数名称获取对应的函数和用法信息
    if function_to_run in function_mappings:
        func, usage_message = function_mappings[function_to_run]
        inputs = parse_args(4, usage_message)
        try:
            # 对于 test_number_error 需要将 Limit 转换为 int
            if function_to_run == 'test_number_error':
                inputs = (inputs[0], int(inputs[1]))
            result = func(*inputs)
            if result is not None:  # 如果函数返回结果，则打印它
                print(result)
        except ValueError as e:
            print(e)
            sys.exit(1)
    else:
        print("无效的函数。请选择 test_number_error, test_picupdate 或 test_pdf 作为第一个参数。")
        sys.exit(1)

    # 检查目录是否存在
    if os.path.exists(home):
        # 删除目录及其所有内容
        shutil.rmtree(home)

if __name__ == "__main__":
    main()
