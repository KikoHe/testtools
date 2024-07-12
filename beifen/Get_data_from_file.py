import os, ast

### 文件操作 ###

# 获取当前目录
current_dir = os.getcwd()
# 列出当前目录中所有文件
files = os.listdir(current_dir)

# 创建一个空列表，用于存储所有直接结果不为空的数据
merged_data = []

# 遍历文件列表
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

