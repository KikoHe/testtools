import os, ast
from Test_case import *
##### Debug测试脚本合集

# 获取当前目录
current_dir = os.getcwd()

folder_path = '/Users/ht/Desktop/PythonTools/Pic_Test/Pic/'
if os.path.exists(folder_path):
    delete_folder(folder_path)


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

# 多任务同时执行
def multi_action_test():
    address = "PBN"
    offsets = [0, 5000, 10000, 15000, 20000]
    limit = 5000
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

# 测试素材
def test_ids():
    # ids = ['63e4b86cd32ec78307fbb7f2', '638dbc678bbc0a11d3226a97', '63f5e359530c3bd9785385af', '63ef4967af7d576d8b1f3b02', '65f2e7d0296812e63bf122ab']
    ids = ['66a07055199ee18ff49d5e52','669741b3db160c6f51366697','668b891ecd6bcc4ded4f5cd2']
    error_ids = []
    for id in ids:
        print(id)
        test_result = test_single_pic(id, "PBN")
        if test_result == False:
            error_ids.append(id)
    print("error!!!!!!!!!!"+str(error_ids))

if __name__ == "__main__":
    # multi_action_test()   # 测试到3544
    test_ids()

