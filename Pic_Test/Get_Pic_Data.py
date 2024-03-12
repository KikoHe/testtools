import pytz, hashlib, zipfile, os, requests
from datetime import datetime
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

### 获取所有项目今天更新的图库页、Daily页的素材ID、zip_url
def get_today_update_lib_or_daily_pic_data(address, limit=30, timezone=timezone, group="default"):
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
    pic_data = {}
    response_data = {}
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    if response_data == {}:
        print("列表数据请求失败： "+str(url)+str(headers))

    elif address.startswith("PBN"):
        paintList = response_data["paintList"]
        for item in paintList:
            if item["releaseDate"] == formatted_date2:
                pic_id = item["id"]
                if "vector_zip_file" in item and item["vector_zip_file"] != None:
                    zip_url = item["vector_zip_file"]
                else:
                    zip_url = item["zip_file"]
                pic_data[pic_id] = zip_url

    elif address.startswith(("VC", "ZC", "BP", "Vista")):
        content = response_data["content"]
        for detail_content in content:
            if (address in ["VC_Daily", "ZC_Daily", "Vista_Daily"] and detail_content["daily"] == formatted_date1) or \
                    (address in ["VC_Lib", "ZC_Lib", "Vista_Lib"] and detail_content["logic"]["release_date"] == formatted_date2):
                    zip_url = detail_content["detail"][0]["resource"]["zip"]
                    pic_id = detail_content["detail"][0]["id"]
                    pic_data[pic_id] = zip_url
            elif (address in ["BP_Lib"] and detail_content["relase_date"] == formatted_date2) or \
                    (address in ["BP_Daily"] and str(detail_content["daily"]) == formatted_date2):  # 这里就是错误的relase_date拼写
                    zip_url = detail_content["zip_2048_pdf"]
                    pic_id = detail_content["id"]
                    pic_data[pic_id] = zip_url
    return pic_data

### 获取PBN、BP所有方案今天更新的素材是否一致，如果一致，则返回当天更新的素材数据
def get_all_imagegroup_pic_update(address):
    update_pic_data = {}
    update_pic_number = []
    if address.startswith("BP"):
        group_list = ["default", "default_ios", "test_a"]
    elif address.startswith("PBN"):
        group_list = ["c", "ios_c", "us-new", "vietnam-new", "brazil-new", "india-new", "mexico-new"]
    else:
        group_list = ["default"]
    for group in group_list:
        update_pic_data = get_today_update_lib_or_daily_pic_data(address, limit=50, timezone=timezone, group=group)
        update_pic_number.append(len(update_pic_data))
    if all(x == update_pic_number[0] for x in update_pic_number):
        return update_pic_data
    else:
        different_update_group = [i for i, x in enumerate(update_pic_number) if x != update_pic_number[0]]
        fail_group_list = []
        for number in different_update_group:
            fail_group = group_list[number]
            fail_group_list.append(fail_group)
            print("以下素材方案更新的素材数量有问题: ", str(fail_group_list))
        return False

### 获取PBN某个时区最新的故事线ID和里面的素材信息
def get_lastest_story_pic_data(time_zone):
    story_list_url = f"https://paint-api.dailyinnovation.biz/paint/v1/today?install_day=1681&explore_simplified=0&day=1681&groupNumber=c"
    headers_timezone = {
        "platform": "android",
        "install_day": "100",
        "timezone": time_zone,
        "today": formatted_date2,
        "country": "US",
        "version": "4.4.10",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.4.10"
    }
    lastest_story_id = []
    lastest_story_pic_data = {}
    try:
        response = session.get(story_list_url, headers=headers_timezone)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        lastest_story_id = response.json()["data"][1]["newChallengeList"][0]["id"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    story_detail_url = f"https://paint-api.dailyinnovation.biz/paint/v1/story/{lastest_story_id}"

    try:
        response = session.get(story_detail_url, headers=headers_timezone)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        for paintList in response_data["paintList"]:
            pic_id = paintList["id"]
            zip_url = paintList["vector_zip_file"]
            lastest_story_pic_data[pic_id] = zip_url

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return lastest_story_id, lastest_story_pic_data
### 获取更新的故事线素材（通过对比0、8两个时区）
def get_today_uptate_story_pic_data():
    story_id_0, story_pic_data_0 = get_lastest_story_pic_data(timezone)
    story_id_8, story_pic_data_8 = get_lastest_story_pic_data(timezone_cn)
    if story_id_0 != story_id_8:
        print("今天上了新的故事线！")
        update_story_pic_data = story_pic_data_0
    else:
        update_story_pic_data = {key: story_pic_data_0[key] for key in story_pic_data_0 if key not in story_pic_data_8}
    print("今天上新的素材： "+str(update_story_pic_data))
    return update_story_pic_data

# 获取Vista某个时区最新3个的内购包里面的素材信息
def get_lastest_pack_pic_data(time_zone):
    pack_list_url = "https://colorpad-api.vitastudio.ai/colorpad/v1/paint/pack?limit=3"
    headers = {
        "platform": "ios",
        "install_day": "100",
        "timezone": time_zone,
        "today": formatted_date2,
        "country": "US",
        "version": "4.4.10",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
    }
    lastest_pack_pic_data = {}
    try:
        response = session.get(pack_list_url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        for data in response_data["content"]:
            paints = data["paints"]
            for paints_data in paints:
                lastest_pack_pic_data[paints_data["detail"][0]["id"]] = paints_data["detail"][0]["resource"]["zip"]
        return lastest_pack_pic_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
# 获取更新的内购包里面的素材信息
def get_today_update_pack_pic_data():
    pack_pic_data_0 = get_lastest_pack_pic_data(timezone)
    pack_pic_data_8 = get_lastest_pack_pic_data(timezone_cn)
    update_pack_pic_data = {}
    for key, value in pack_pic_data_0.items():
        if key not in pack_pic_data_8:
            update_pack_pic_data[key] = value
    return update_pack_pic_data

# 获取对应素材的zip包，解压并获得包内文件
def get_zip_detail(address, pic_id, zip_url):
    # 计算密码
    if address.startswith("BP"):
        pwd = "UHVnW2k9QWY3Smp2cGZIYldOdGt2eXZOcUt1dFQpOEY="
    else:
        passwordid = pic_id + "VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
        pwd = hashlib.md5(passwordid.encode()).hexdigest()
    # 创建下载目录
    if os.path.exists(home) == False:
        os.mkdir(home)
    # 下载zip包
    try:
        with session.get(zip_url, stream=True, timeout=(10, 30)) as zip_r:
            zip_r.raise_for_status()
            filename = os.path.join(home, f"{pic_id}.zip")

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
            zf.extract(name, './%s/%s' % ("Pic", pic_id))
        zf.close()
    except zipfile.BadZipFile as e:
        print(f"文件损坏，无法解压: {e}")
