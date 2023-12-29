from datetime import datetime
import json,pytz
import requests
import hashlib, zipfile, os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
timezone = "Pacific/Apia"
timezone_cn = "Asia/Shanghai"
today = datetime.now(pytz.timezone(timezone))
formatted_date1 = today.strftime("%Y-%m-%d")
formatted_date2 = today.strftime("%Y%m%d")
formatted_date3 = today.strftime("%Y%m") ##当前月份

home = os.path.join(os.getcwd(), "Pic")  ##下载的zip文件存放路径

# 设置重试次数以及回退策略
retries = Retry(total=5,  # 总尝试次数
                backoff_factor=1,  # 回退等待时间的指数基数
                status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

# 创建一个带有重试的会话对象
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))

def Get_storyid(timezone_country):
    ###获取不同时区下的最新的故事线ID
    PBN_Today_url = f"https://paint-api.dailyinnovation.biz/paint/v1/today?install_day=1681&explore_simplified=0&day=1681&groupNumber=c"
    headers = {
        "platform": "android",
        "install_day": "100",
        "timezone": timezone_country,
        "today": formatted_date2,
        "country": "US",
        "version": "4.4.10",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.4.10"
    }
    try:
        response = session.get(PBN_Today_url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        return response_data[1]["newChallengeList"][0]["id"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurredGet_storyid: {err}")

def Get_story_pic(timezone_country):
    ###获取不同时区下最新故事线的素材ID
    stroyid = Get_storyid(timezone_country)
    PBN_story_url = f"https://paint-api.dailyinnovation.biz/paint/v1/story/{stroyid}"
    headers = {
        "platform": "android",
        "install_day": "100",
        "timezone": timezone_country,
        "today": formatted_date2,
        "country": "US",
        "version": "4.4.10",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.4.10"
    }
    pic_id_zipurl = {}
    try:
        response = session.get(PBN_story_url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        for paintList in response_data["paintList"]:
            pic_id_zipurl[paintList["id"]] = paintList["vector_zip_file"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return pic_id_zipurl

def Get_stroyupdatepicid():
    ###获取更新的故事素材ID和zipurl
    stroyid = Get_storyid(timezone)
    stroyid_cn = Get_storyid(timezone_cn)
    stroypic = Get_story_pic(timezone)
    stroypic_cn = Get_story_pic(timezone_cn)
    if stroyid != stroyid_cn:
        # print("上了新的故事线，故事线ID：" + stroyid)
        stroyupdatepic = stroypic
    else:
        stroyupdatepic = {key: stroypic[key] for key in stroypic if key not in stroypic_cn}
        # if stroyupdatepicid:
        #     print("未上新故事线，仅更新素材，故事线ID：" + stroyid + "更新素材ID：" + stroyupdatepicid)
        # else:
        #     print("未更新素材")
    return stroyupdatepic

def Get_List(address, limit=10, timezone=timezone):
    # 获取以下列表的数据
    url_prefixes = {
        "ZC_Lib": f"https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?limit={limit}",
        "ZC_Daily": f"https://api.colorflow.app/colorflow/v1/daily?query_date={formatted_date1}",
        "VC_Lib": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paintcategory/all/paints?limit={limit}",
        "VC_Daily": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/daily?query_date={formatted_date1}",
        "PBN_Lib": f"https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5ba31d31fe401a000102966e/paints?day=100&limit={limit}",
        "PBN_Daily": f"https://paint-api.dailyinnovation.biz/paint/v1/daily?groupNumber=c&day=0&limit=400&offset=0",
        "BP_Lib": f"https://bpbnapi.idailybread.com/paint/v1/paintCategory/trending/list?limit={limit}&offset=0&day=502&group_key\
        =test_a&isAddDayMax=false&read_unactive=false&time_date=1703746118589&sort_plan=normal",
        "BP_Daily": f"https://bpbnapi.idailybread.com/paint/v1/daily/{formatted_date3}"
    }

    headers = {
        "platform": "android",
        "install_day": "100",
        "timezone": timezone,
        "today": formatted_date2,
        "country": "US",
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


def Get_Picid(address,limit):
    data = Get_List(address,limit)
    Pic_ids = []
    if address.startswith("PBN"):
        paintList = data["paintList"]
        for item in paintList:
            if item["releaseDate"] == formatted_date2:
                Pic_ids.append(item["id"])

    elif address.startswith(("VC", "ZC", "BP")):
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
            elif address in ["BP_Lib"]:
                relesedate = detail_content["relase_date"]
                if relesedate == formatted_date2:
                    Pic_ids.append(detail_content[0]["id"])
            elif address in ["BP_Daily"]:
                relesedate = detail_content["daily"]
                if relesedate == formatted_date2:
                    Pic_ids.append(detail_content[0]["id"])
    return Pic_ids


def Get_id_Zipurl(address, limit):
    data = Get_List(address, limit)
    Pic_ids = []
    Zip_url = []
    if address.startswith("PBN"):
        paintList = data["paintList"]
        for item in paintList:
            if item["releaseDate"] == formatted_date2:
                Zip_url.append(item["vector_zip_file"])
                Pic_ids.append(item["id"])

    elif address.startswith(("VC", "ZC", "BP")):
        content = data["content"]
        for detail_content in content:
            if address in ["VC_Daily", "ZC_Daily"]:
                if detail_content["daily"] == formatted_date1:
                    Zip_url.append(detail_content["detail"][0]["resource"]["zip"])
                    Pic_ids.append(detail_content["detail"][0]["id"])
            elif address in ["VC_Lib", "ZC_Lib"]:
                if detail_content["logic"]["release_date"] == formatted_date2:
                    Zip_url.append(detail_content["detail"][0]["resource"]["zip"])
                    Pic_ids.append(detail_content["detail"][0]["id"])
            elif address in ["BP_Lib"]:
                if detail_content["relase_date"] == formatted_date2:
                    Zip_url.append(detail_content["zip_2048_pdf"])
                    Pic_ids.append(detail_content["id"])
            elif address in ["BP_Daily"]:
                if str(detail_content["daily"]) == formatted_date2:
                    Zip_url.append(detail_content["zip_2048_pdf"])
                    Pic_ids.append(detail_content["id"])
    return Pic_ids, Zip_url

def Get_Zip(PicID, Zip_url, address):
    # 计算密码
    if address.startswith("BP"):
        pwd = "UHVnW2k9QWY3Smp2cGZIYldOdGt2eXZOcUt1dFQpOEY="
    else:
        passwordid = PicID + "VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
        pwd = hashlib.md5(passwordid.encode()).hexdigest()
    #创建下载目录
    if os.path.exists(home) == False:
        os.mkdir(home)

    # 下载zip包
    try:
        with session.get(Zip_url, stream=True, timeout=(10, 30)) as zip_r:
            zip_r.raise_for_status()
            filename = os.path.join(home, f"{PicID}.zip")

            # 安全地删除已存在的文件
            if os.path.exists(filename):
                os.remove(filename)

            # 流式写入文件
            with open(filename, "wb") as code:
                for chunk in zip_r.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        code.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"请求ZIP包时发生错误: {e}")
        return

    try:
        # 确保文件已经完整下载再进行解压
        zf = zipfile.ZipFile(filename)
        zf.setpassword(pwd.encode())
        for name in zf.namelist():
            zf.extract(name, './%s/%s' % ("Pic", PicID))
        zf.close()
    except zipfile.BadZipFile as e:
        print(f"文件损坏，无法解压: {e}")

def Get_detailjson(PicID, Zip_url, address):
    Get_Zip(PicID, Zip_url, address)
    if address.startswith("BP"):
        filename = home + "/" + str(PicID) + "/" + "data.json"
    else:
        filename = home + "/" + str(PicID) + "/" + "detail.json"
    with open(filename, "r") as file:
        data = json.load(file)
        return data

def Get_PDF(PicID, Zip_url, address):
    ###获取PDF资源
    Get_Zip(PicID, Zip_url, address)
    if address.startswith("BP"):
        pic_pdf_path = os.path.join(home, str(PicID), "origin.pdf")
        return pic_pdf_path
    else:
        pic_region_path = os.path.join(home, str(PicID), f"{PicID}_origin")
        pic_pdf_path = f"{pic_region_path}.pdf"
        if os.path.exists(pic_region_path):
            os.rename(pic_region_path, pic_pdf_path)
            return pic_pdf_path

def Get_Number_From_Center(data):
    center_number_code_list = []
    if "center" in data:
        center = data["center"]
        center_number = center.split('|')  # 色块数
        for i in range(len(center_number)):
            center_number_code = center_number[i - 1].split(',')[0]
            center_number_code_int = int(center_number_code)
            center_number_code_list.insert(-1, center_number_code_int)
    return sorted(center_number_code_list)

def Get_Number_From_Plan(data, address):
    plan_number_code_list = []
    plan = []
    if address.startswith("BP"):
        if "color" in data:
            plan = data["color"]
    else:
        if "plans" in data:
            plan = data["plans"]
    if plan != []:
        plan_number = plan[0].split('|')  # 色号数
        for i in range(len(plan_number)):
            plan_number_code = plan_number[i].split('#')[0].split(',')
            for num in range(len(plan_number_code)):
                plan_number_code_single = plan_number_code[num - 1]
                plan_number_code_int = int(plan_number_code_single)
                plan_number_code_list.insert(-1, plan_number_code_int)
    return sorted(plan_number_code_list)
