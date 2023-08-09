import hashlib,argparse,os

def Get_MD5(file_path):
    file_name = os.path.basename(file_path)
    id = file_name.split("_")
    pwd_test = id[0] + "VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
    password = hashlib.md5(pwd_test.encode('utf-8')).hexdigest()
    print("PICID: " + id[0])
    print("MD5: " + password)

parser = argparse.ArgumentParser(description='获取MD5值')
parser.add_argument('file', type=str, help='检测文件名称')

args = parser.parse_args()

# 获取文件路径参数
file_path = args.file
# 检查文件格式
Get_MD5(file_path)

