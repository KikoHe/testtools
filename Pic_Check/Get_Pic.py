import json, pytz, hashlib, zipfile, os, requests, fitz
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# from Get_Pic_By_Other import *


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

# 获取素材列表的数据
def Get_List(address, limit=10, timezone=timezone, group="default"):
    url_prefixes = {
        "ZC_Lib": f"https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?limit={limit}",
        "ZC_Daily": f"https://api.colorflow.app/colorflow/v1/daily?query_date={formatted_date1}",
        "VC_Lib": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paintcategory/all/paints?limit={limit}",
        "VC_Daily": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/daily?query_date={formatted_date1}",
        "PBN_Lib": f"https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5ba31d31fe401a000102966e/paints?day=100&limit={limit}&groupNumber={group}",
        "PBN_Daily": f"https://paint-api.dailyinnovation.biz/paint/v1/daily?groupNumber=c&day=0&limit=400&offset=0",
        "BP_Lib": f"https://bpbnapi.idailybread.com/paint/v1/paintCategory/trending/list?limit={limit}&offset=0&day=503&group_key={group}&isAddDayMax=false&read_unactive=false&time_date=1709027222&sort_plan=normal",
        "BP_Daily": f"https://bpbnapi.idailybread.com/paint/v1/daily/{formatted_date3}",
        "Vista_Lib": f"https://colorpad-api.vitastudio.ai/colorpad/v1/paintcategory/all/paints?offset=0&limit={limit}",
        "Vista_Daily": f"https://colorpad-api.vitastudio.ai/colorpad/v1/daily?query_date={formatted_date1}"
    }
    headers = {
        "platform": "android",
        "image_group": group,
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

# 获取Get_List列表数据中图片ID和zip包url
def Get_id_Zipurl(address, limit, group="c"):
    Pic_ids = []
    Zip_url = []
    attempt_count = 0
    while True:
        data = Get_List(address, limit, timezone, group)
        if address.startswith("PBN"):
            Pic_ids.clear()  # 清除之前的内容
            Zip_url.clear()
            paintList = data["paintList"]
            for item in paintList:
                if item["releaseDate"] == formatted_date2:
                    if item["vector_zip_file"] == None:
                        Zip_url.append(item["zip_file"])
                        # print(item["id"])
                    else:
                        Zip_url.append(item["vector_zip_file"])
                    Pic_ids.append(item["id"])
            # 检查Pic_ids长度是否满足条件
            if len(Pic_ids) == 15 or attempt_count >= 2:
                break  # 如果满足条件或已经尝试了3次，则结束循环
            attempt_count += 1
        elif address.startswith(("VC", "ZC", "BP", "Vista")):
            content = data["content"]
            for detail_content in content:
                if address in ["VC_Daily", "ZC_Daily", "Vista_Daily"]:
                    if detail_content["daily"] == formatted_date1:
                        Zip_url.append(detail_content["detail"][0]["resource"]["zip"])
                        Pic_ids.append(detail_content["detail"][0]["id"])
                elif address in ["VC_Lib", "ZC_Lib", "Vista_Lib"]:
                    # if detail_content["logic"]["release_date"] == formatted_date2:
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
            break
    # print(len(Pic_ids))
    return Pic_ids, Zip_url

# 获取不同的素材实验方案的素材数据，判断是否有方案的素材有缺失
def Get_all_group_Lib_list_pic_ids(address,limit, group_list):
    group_ids = []
    for group in group_list:
        ids, _ = Get_id_Zipurl(address, limit, group)
        group_ids.append(len(ids))

    # 寻找结果数量不是最大数量的所有group
    max_count = max(group_ids)
    inconsistent_groups = [group_list[i] for i in range(len(group_list)) if group_ids[i] != max_count]
    if inconsistent_groups:
        return inconsistent_groups
    else:
        return group_ids[0]

# 检查BP和PBN项目的素有素材实验
def Get_all_project_Lib_list_pic_ids(address,limit):
    ids = []
    group_list_bp = ["default", "default_ios", "test_a"]
    group_list_pbn = ["c", "ios_c", "us-new", "vietnam-new", "brazil-new", "india-new", "mexico-new"]
    if address == "BP_Lib":
        ids = Get_all_group_Lib_list_pic_ids(address, limit, group_list_bp)
    elif address == "PBN_Lib":
        ids = Get_all_group_Lib_list_pic_ids(address, limit, group_list_pbn)
    return ids


# 获取最新的故事线ID
def Get_storyid(timezone_country):
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

# 获取PBN最新故事线的素材ID
def Get_story_pic(timezone_country):
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

# 获取PBN更新的故事素材数据（通过不同时区返回不同数据来获取）
def Get_stroyupdatepicid():
    stroyid = Get_storyid(timezone)
    stroyid_cn = Get_storyid(timezone_cn)
    stroypic = Get_story_pic(timezone)
    stroypic_cn = Get_story_pic(timezone_cn)
    if stroyid != stroyid_cn:
        stroyupdatepic = stroypic
    else:
        stroyupdatepic = {key: stroypic[key] for key in stroypic if key not in stroypic_cn}
    ids = list(stroyupdatepic.keys())
    Zip_url = list(stroyupdatepic.values())
    return ids,Zip_url

# 获取Vista所有内购包的素材数据
def Get_Pack_Pic_Data(timezone_country):
    Vista_Pack_url = "https://colorpad-api.vitastudio.ai/colorpad/v1/paint/pack"
    # Vista_Pack_url = "https://colorpad-api-stage.vitastudio.ai/colorpad/v1/paint/pack?limit=50" #测试数据
    headers = {
        "platform": "ios",
        "install_day": "100",
        "timezone": timezone_country,
        "today": formatted_date2,
        "country": "US",
        "version": "4.4.10",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
    }
    pic_data = []
    try:
        response = session.get(Vista_Pack_url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        for data in response_data["content"]:
            paints = data["paints"]
            for paints_data in paints:
                paint_dict = {
                   paints_data["detail"][0]["id"]: paints_data["detail"][0]["resource"]["zip"]
                }
                pic_data.append(paint_dict)
        return pic_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 获取Vista内购包模块更新的素材数据
def Get_Pack_Pic_Update_Data():
    pic_data = Get_Pack_Pic_Data(timezone)
    pic_data_cn = Get_Pack_Pic_Data(timezone_cn)
    # pic_data_cn = Get_Pack_Pic_Data("America/Los_Angeles") #测试数据
    update_data = [element for element in pic_data if element not in pic_data_cn]
    ids = [list(d.keys())[0] for d in update_data]  # 提取所有的键
    url = [list(d.values())[0] for d in update_data]
    return ids, url

# 根据图片url下载素材zip包内容
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

# 调用Get_Zip方法，然后获取素材detailjson内的数据
def Get_detailjson(PicID, Zip_url, address):
    Get_Zip(PicID, Zip_url, address)
    if address.startswith("BP"):
        filename = home + "/" + str(PicID) + "/" + "data.json"
    else:
        filename = home + "/" + str(PicID) + "/" + "detail.json"
    with open(filename, "r") as file:
        data = json.load(file)
        return data

# 调用Get_Zip方法，然后获取素材PDF数据
def Get_PDF(PicID, Zip_url, address):
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

# 检查PDF是否遮挡了色号显示的位置
def Check_Pdf_Block(pdf_file, ids_, Zip_url_, address):
    doc = fitz.open(pdf_file)
    page = doc[0]

    data = Get_detailjson(ids_, Zip_url_, address)
    Axis_list = Get_Axis_From_Center(data)

    Failed_Axis = []
    for Axis in Axis_list:
        x, y, radius = Axis[0], Axis[1], Axis[2]
        x1, y1 = float(x) - float(radius), float(y) - float(radius)
        x2, y2 = float(x) + float(radius), float(y) + float(radius)
        bbox = fitz.Rect(x1, y1, x2, y2)
        if int(radius) < 5:
            # print(x, y, radius)
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), clip=bbox)
            pixel_value = int.from_bytes(pix.samples, byteorder='big')
            if pixel_value < 255:
                Failed_Axis.append(Axis)
    if Failed_Axis == []:
        return True
    else:
        print(Failed_Axis)
        return False

# print(Check_Pdf_Block("/Users/ht/Desktop/PythonTools/Pic_Check/Pic/654da6d861b9c94253eba131/1141b9babfd990c283132c7cb5620283.pdf",917,3,2))

# 根据detailjson数据，获取其中的center数据中的色块编号
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

def Get_Axis_From_Center(data):
    center_number_Axis_list = []
    if "center" in data:
        center = data["center"]
        if center != None:
            center_number = center.split('|')  # 色块数
            for i in range(len(center_number)):
                center_number_code_x = center_number[i - 1].split(',')[1]
                center_number_code_y = center_number[i - 1].split(',')[2]
                center_number_code_radius = center_number[i - 1].split(',')[3]
                center_number_Axis = [center_number_code_x,
                    center_number_code_y,
                    center_number_code_radius]
                center_number_Axis_list.append(center_number_Axis)
        else:
            print("No center")
    return center_number_Axis_list

# 根据detailjson数据，获取其中的float center数据中的色块编号
def Get_Number_From_FloatCenter(data):
    center_number_code_list = []
    if "center_float" in data:
        center = data["center_float"]
        if center != None:
            center_number = center.split('|')  # 色块数
            for i in range(len(center_number)):
                center_number_code = center_number[i - 1].split(',')[0]
                center_number_code_int = int(center_number_code)
                center_number_code_list.insert(-1, center_number_code_int)
        else:
            print("No center_float")
    return sorted(center_number_code_list)

def Get_Axis_From_FloatCenter(data):
    center_number_Axis_list = []
    if "center_float" in data:
        center = data["center_float"]
        if center != None:
            center_number = center.split('|')  # 色块数
            for i in range(len(center_number)):
                center_number_code_x = center_number[i - 1].split(',')[1]
                center_number_code_y = center_number[i - 1].split(',')[2]
                center_number_code_radius = center_number[i - 1].split(',')[3]
                center_number_Axis = {
                    center_number_code_x,
                    center_number_code_y,
                    center_number_code_radius
                }
                center_number_Axis_list.append(center_number_Axis)
        else:
            print("No center_float")
    return center_number_Axis_list

# 根据detailjson数据，获取其中的plan数据中的色块编号
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
        # print("start")
        plan_number = plan[0].split('|')   # 色块信息
        Number = 1
        for i in range(len(plan_number)):
            plan_number_code = plan_number[i].split('#')[0].split(',')
            for num in range(len(plan_number_code)):
                plan_number_code_single = plan_number_code[num - 1]
                plan_number_code_int = int(plan_number_code_single)
                # if plan_number_code_int == "1185":   ###返回色块编号为plan_number_code_int的色号编号
                #     print(Number) # 色号数
                plan_number_code_list.insert(-1, plan_number_code_int)
            Number = Number + 1
    return sorted(plan_number_code_list)

# 根据detailjson数据，获取其中的数据中的area数据：色块外切矩形的坐标,然后对比center中的数字位置，是否在area区域内
def Test_area_and_Center(data):
    if "area" in data and "center" in data:
        area_data = data["area"]
        center = data["center"]

        if area_data != None and center != None:
            center_number = center.split('|')  # 色块数
            failed_numebr = []
            for i in range(len(center_number)):
                center_number_code = center_number[i - 1].split(',')[0]
                center_number_code_x = center_number[i - 1].split(',')[1]
                center_number_code_y = center_number[i - 1].split(',')[2]
                center_number_code_int_x = float(center_number_code_x)
                center_number_code_int_y = float(center_number_code_y)

                if center_number_code in area_data:
                    area_data_number = area_data[center_number_code]

                    xmin = area_data_number["minX"]
                    xmax = area_data_number["maxX"]
                    ymin = area_data_number["minY"]
                    ymax = area_data_number["maxY"]
                    if xmin < center_number_code_int_x < xmax and ymin < center_number_code_int_y < ymax:
                        pass
                    else:
                        failed_numebr.append(int(center_number_code))
            if failed_numebr != []:
                print(sorted(failed_numebr))
                return False
            else:
                return True
        else:
            print("No center_float")
            return True
    else:
        return True
# 对比centerfloat
def Test_area_and_FloatCenter(data):
    if "center_float" in data:
        area_data = data["area"]
        center = data["center_float"]
        if area_data != None and center != None:
            center_number = center.split('|')  # 色块数
            failed_numebr = []
            for i in range(len(center_number)):
                center_number_code = center_number[i - 1].split(',')[0]
                center_number_code_x = center_number[i - 1].split(',')[1]
                center_number_code_y = center_number[i - 1].split(',')[2]
                center_number_code_int_x = float(center_number_code_x)
                center_number_code_int_y = float(center_number_code_y)

                if center_number_code in area_data:
                    area_data_number = area_data[center_number_code]

                    xmin = area_data_number["minX"]
                    xmax = area_data_number["maxX"]
                    ymin = area_data_number["minY"]
                    ymax = area_data_number["maxY"]
                    if xmin < center_number_code_int_x < xmax and ymin < center_number_code_int_y < ymax:
                        pass
                    else:
                        failed_numebr.append(int(center_number_code))
            if failed_numebr != []:
                print(sorted(failed_numebr))
                return False
            else:
                return True
        else:
            print("No center_float")
            return True
    else:
        return True