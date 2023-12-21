from datetime import datetime
import json,pytz
import requests
import hashlib, zipfile, os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
timezone = "Pacific/Apia"
today = datetime.now(pytz.timezone(timezone))
formatted_date1 = today.strftime("%Y-%m-%d")
formatted_date2 = today.strftime("%Y%m%d")

home = os.path.join(os.getcwd(), "Pic")  ##下载的zip文件存放路径


def Get_List(address, limit):
    # 设置重试次数以及回退策略
    retries = Retry(total=5,  # 总尝试次数
                    backoff_factor=1,  # 回退等待时间的指数基数
                    status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

    # 创建一个带有重试的会话对象
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))

    # 获取列表数据
    # today = datetime.now()
    # formatted_date1 = today.strftime("%Y-%m-%d")
    # formatted_date2 = today.strftime("%Y%m%d")

    url_prefixes = {
        "ZC_Lib": f"https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?limit={limit}",
        "ZC_Daily": f"https://api.colorflow.app/colorflow/v1/daily?query_date={formatted_date1}",
        "VC_Lib": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paintcategory/all/paints?limit={limit}",
        "VC_Daily": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/daily?query_date={formatted_date1}",
        "PBN_Lib": f"https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5ba31d31fe401a000102966e/paints?day=100&limit={limit}",
        "PBN_Daily": f"https://paint-api.dailyinnovation.biz/paint/v1/daily?groupNumber=c&day=0&limit=400&offset=0"
    }

    headers = {
        "platform": "android",
        "install_day": "100",
        "timezone": timezone,
        "today": formatted_date2,
        "country": "CN",
        "version": "4.4.10",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.4.10"
    }

    url = url_prefixes.get(address)

    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    # print(response_data)

def Get_Picid(address,limit):
    data = Get_List(address,limit)
    # print(data)
    Pic_ids = []
    if address.startswith("PBN"):
        paintList = data["paintList"]
        for item in paintList:
            if item["releaseDate"] == formatted_date2:
                Pic_ids.append(item["id"])

    elif address.startswith(("VC", "ZC")):
        content = data["content"]
        for detail_content in content:
            if address in ["VC_Daily", "ZC_Daily"]:
                relesedate = detail_content["daily"]
                if relesedate == formatted_date1:
                    Pic_ids.append(detail_content["detail"][0]["id"])
            elif address in ["VC_Lib", "ZC_Lib"]:
                relesedate = detail_content["logic"]["release_date"]
                if relesedate == formatted_date2:
                    Pic_ids.append(detail_content["detail"][0]["id"])
    return Pic_ids

def Get_Zip(PicID, address):
    #获取素材详情地址，并下载zip资源
    url_prefixes = {
        "ZC_Daily": "https://api.colorflow.app/colorflow/v1/paint/",
        "ZC_Lib": "https://api.colorflow.app/colorflow/v1/paint/",
        "PBN_Lib": "https://paint-api.dailyinnovation.biz/paint/v1/paint/",
        "PBN_Daily": "https://paint-api.dailyinnovation.biz/paint/v1/paint/",
        "VC_Lib": "https://vitacolor-api.vitastudio.ai/vitacolor/v1/paint/",
        "VC_Daily": "https://vitacolor-api.vitastudio.ai/vitacolor/v1/paint/"
    }
    url_Pre = url_prefixes.get(address, "https://paint-api.dailyinnovation.biz/paint/v1/paint/")
    url = url_Pre + PicID
    headers = {"platform": "ios"}
    response = requests.get(url, headers=headers)
    if address.startswith("PBN"):
        zip = response.json()["data"]["vector_zip_file"]
    elif address.startswith(("VC", "ZC")):
        zip = response.json()["data"]["resource"]["zip"]

    # 计算密码
    passwordid = PicID + "VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
    pwd = hashlib.md5(passwordid.encode()).hexdigest()

    #创建下载目录
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

def Get_detailjson(PicID, address):
    Get_Zip(PicID, address)
    filename = home + "/" + str(PicID) + "/" + "detail.json"
    with open(filename, "r") as file:
        data = json.load(file)
        return data

def Get_PDF(PicID, address):
    Get_Zip(PicID, address)
    pic_region_path = os.path.join(home, str(PicID), f"{PicID}_origin")
    pic_pdf_path = f"{pic_region_path}.pdf"
    if os.path.exists(pic_region_path):
        os.rename(pic_region_path,pic_pdf_path)
        return pic_pdf_path

# Get_Zip("6581275191c3e3b9171f09fd", "VC_Daily")

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
