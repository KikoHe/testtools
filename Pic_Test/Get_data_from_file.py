import os, ast
from Test_case import *
##### Debug测试脚本合集

# 获取当前目录
current_dir = os.getcwd()

### 文件操作 ###
def merged_data():
    files = os.listdir(current_dir)
    merged_data = []
    for file in files:
        if file.startswith("output_"):
            with open(file, 'r') as f:
                content = f.read()
                result = ast.literal_eval(content.split("：")[1])
                result = [item for item in result if item]
                merged_data.extend(result)
    # 将合并后的数据写入新文件
    with open("Test_Result/merged_output.txt", 'w') as new_file:
        for item in merged_data:
            new_file.write(str(item) + '\n')
    print("合并后的数据已写入到 merged_output.txt 文件中。")

# 测试素材
def test_ids():
    ids = ['657a8300c14c58ea92aeac88']
    error_ids = []
    for id in ids:
        print(id)
        test_result = test_single_pic(id, "PBN")
        if test_result == False:
            error_ids.append(id)
    print("error!!!!!!!!!!"+str(error_ids))