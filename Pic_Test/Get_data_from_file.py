import os, ast, re
from Test_case import *
##### Debug测试脚本合集

# 获取当前目录
current_dir = os.getcwd()

folder_path = '/Users/ht/Desktop/PythonTools/Pic_Test/Pic/'
if os.path.exists(folder_path):
    delete_folder(folder_path)

### 合并output_操作 ###
def merged_data():
    files = os.listdir(current_dir)
    merged_data = []
    for file in files:
        if file.startswith("output_"):
            with open(file, 'r') as f:
                content = f.read()
                result = re.findall(r'[0-9a-fA-F]{24}', content)
                merged_data.extend(result)
    # 将合并后的数据写入新文件
    with open("Test_Result/merged_output.txt", 'w') as new_file:
        for item in merged_data:
            new_file.write(str(item) + '\n')
    print("合并后的数据已写入到 merged_output.txt 文件中。")

# 多任务同时执行
def multi_action_test():
    address = "PBN"
    offsets = [6000, 8000, 10000, 12000, 14000]
    limit = 2000
    args = [(address, offset, limit) for offset in offsets]

    with multiprocessing.Pool() as pool:
        pool.starmap(test_pic_from_cms, args)

### 从excel中获取ID
def get_picid_from_excel(address, filename):
    df = pd.read_excel(filename, usecols=[0])
    data = df.to_dict(orient='split')
    json_data = {
        'columns': data['columns'],
        'data': data['data']
    }
    with open('excel/output.json', 'w') as f:
        json.dump(json_data, f)
    Pic_ids = []
    for data in json_data["data"]:
        pic_id = data[0]
        Pic_ids.append(pic_id)
    return Pic_ids


### 从txt中获取ID，生成list
def get_picid_from_text():
    # 读取文件内容并将每行数据作为列表元素
    with open('Test_Result/merged_output.txt', 'r') as file:
        data = file.readlines()
    # 去除每行末尾的换行符
    data = [line.strip() for line in data]
    # 输出读取的数据列表
    print(data)
    return data

# 测试素材
def test_ids():
    # ids = get_picid_from_text()
    ids = ['65f2e7d0296812e63bf122ab']
    error_ids = []
    for id in ids:
        print(id)
        test_result = test_single_pic(id, "PBN", 'pdf')
        if test_result == False:
            error_ids.append(id)
            with open(f'output_error_id.txt', 'a') as file:
                file.write(id)  # 写入输出结果到文件中
    print("error!!!!!!!!!!"+str(error_ids))

if __name__ == "__main__":
    multi_action_test()   # 测试到11500
    # merged_data()
    # get_picid_from_text()
    # test_ids()
