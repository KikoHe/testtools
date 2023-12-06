import json
import requests,shutil,sys
import hashlib,zipfile,os

def Get_Zip(PicID, Project):
    #获取素材详情地址，并下载zip资源
    url_prefixes = {
        "ZC": "https://api.colorflow.app/colorflow/v1/paint/",
        "PBN": "https://paint-api.dailyinnovation.biz/paint/v1/paint/",
        "VC": "https://vitacolor-api.vitastudio.ai/vitacolor/v1/paint/"
    }
    url_Pre = url_prefixes.get(Project, "https://paint-api.dailyinnovation.biz/paint/v1/paint/")
    url = url_Pre + PicID
    headers = {"platform": "ios"}
    response = requests.get(url, headers=headers)
    if Project == "PBN":
        zip = response.json()["data"]["vector_zip_file"]
    elif Project in ["ZC", "VC"]:
        zip = response.json()["data"]["resource"]["zip"]

    # 计算密码
    passwordid = PicID + "VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
    pwd = hashlib.md5(passwordid.encode()).hexdigest()

    #创建下载目录
    home = os.getcwd() + "/" + "Pic"
    if os.path.exists(home) == False:
        os.mkdir(home)
        print("mkdir pic dir ~")

    # 下载zip包
    zip_r = requests.get(zip)
    filename = os.path.join(home, f"{PicID}.zip")
    if zip_r.status_code == 200:
        if os.path.exists(filename) == True:
            os.remove(filename)
        with open(filename, "wb") as code:
            code.write(zip_r.content)
    else:
        print(f"请求失败，状态码：{zip_r.status_code}")

    # 解压zip包
    zf = zipfile.ZipFile(filename, mode='r')
    zf.setpassword(pwd.encode())
    for name in zf.namelist():
        f = zf.extract(name, './%s/%s' % ("Pic", PicID))
    zf.close()

    # 打开detal.json
    filename = home + "/" + str(PicID) + "/" + "detail.json"
    with open(filename, "r") as file:
        data = json.load(file)
        return data

def Get_Number_From_Center(data):
    center = data["center"]
    center_number = center.split('|')  # 色块数
    center_number_code_list = []
    for i in range(len(center_number)):
        center_number_code = center_number[i - 1].split(',')[0]
        center_number_code_int = int(center_number_code)
        center_number_code_list.insert(-1, center_number_code_int)
    return sorted(center_number_code_list)

def Get_Number_From_Plan(data):
    plan = data["plans"]
    plan_number = plan[0].split('|')  # 色号数
    plan_number_code_list = []
    for i in range(len(plan_number)):
        plan_number_code = plan_number[i].split('#')[0].split(',')
        for num in range(len(plan_number_code)):
            plan_number_code_single = plan_number_code[num - 1]
            plan_number_code_int = int(plan_number_code_single)
            plan_number_code_list.insert(-1, plan_number_code_int)
    return sorted(plan_number_code_list)


def Test():
    #创建下载目录
    home = os.getcwd() + "/" + "Pic"
    if os.path.exists(home) == False:
        os.mkdir(home)
    print(home)
    shutil.rmtree(home)
# PicID_input = sys.argv[1]
# Project_input = sys.argv[2]
# Get_Zip(PicID_input, Project_input)

# Test()