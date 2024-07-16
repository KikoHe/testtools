import sys
from Test_case import *
# 参数检查和解析函数
def parse_args():
    return sys.argv[2:]

# 函数映射字典
function_mappings = {
    'test_single_pic': (test_single_pic, "用法: python Run.py test_single_pic <PicID> <address>"),
    'test_single_pic_svg': (test_single_pic_svg, "用法: python Run.py test_single_pic_svg <PicID> <address>"),
    'test_picupdate': (test_single_pic_svg, "用法: python Run.py test_single_pic_svg <PicID> <address>"),
    'test_update_pic_single_by_single': (test_update_pic_single_by_single, "用法: python Run.py test_update_pic_single_by_single <address_list>"),
    'test_pic_from_cms': (test_pic_from_cms, "用法: python Run.py test_pic_from_cms <address> <offset> <limit>"),
    'Dist_error_id': (dist_error_id, "用法: python Run.py Dist_error_id <filename>")
}

def main():
    # 获取要运行的函数名称
    function_to_run = sys.argv[1]
    # 根据函数名称获取对应的函数和用法信息
    if function_to_run in function_mappings:
        func, usage_message = function_mappings[function_to_run]
        inputs = parse_args()
        try:
            result = func(*inputs)
            if result is not None:  # 如果函数返回结果，则打印它
                print(result)
        except ValueError as e:
            print(e)
            sys.exit(1)
    else:
        print("无效的函数。")
        sys.exit(1)

    # 检查目录是否存在
    if os.path.exists(home):
        # 删除目录及其所有内容
        shutil.rmtree(home)

if __name__ == "__main__":
    main()
