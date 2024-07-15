import pytz, hashlib, zipfile, os, requests, pyzipper, subprocess
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
CMS_headers = {
    "cookie": '''_ga=GA1.1.1929480831.1691656939; learnings-passport=_sLoatJ7zrLmUuJjAyErLhekSW3RsYzZ2lr6_ZzTsiHgDHFKnnZS0taYmRszx8Wp; isArtist=false; projectIds=[%225b84f58e689998000116d3fd%22%2C%225b892d3a9f9b4e00011d1cf3%22%2C%225e43d79dbfe4170001141436%22]; products=[%225bfb5a2b6ff9950001e9a969%22%2C%225c00dc5713ab060001c19ea0%22%2C%225b18ef419c560300013ddf28%22%2C%225b18f0079c560300013ddf29%22%2C%225e43d79dbfe4170001141436%22%2C%225b84f58e689998000116d3fd%22%2C%225b892d3a9f9b4e00011d1cf3%22%2C%22657953298aa0c540cc3fd85d%22%2C%22655d7180648210324dccb499%22%2C%2264b4c17796b49d036a8d6bb9%22%2C%2264b4c18196b49d036a8d6bba%22%2C%22645b2f85cd911b5ea8511fd6%22%2C%2260385d6148b726000118051b%22%2C%2260385d8448b726000118051c%22]; ajs_anonymous_id=42cd20ca-c89e-49ac-ad60-eb63ead5252c; uac_passport="2|1:0|10:1719804699|12:uac_passport|44:ZjhjY2Y1Y2ZhYmVlNDA4ZjgyN2I0NzdhYzQwNDYyOWY=|07278d3a26be700c22ec6c25569b9c2fcea8b391ea5e95806372d99497d945d3"; _ga_2Z4PFG28RG=GS1.1.1719818527.767.1.1719818529.58.0.0; learnings-user=Y9TMYRYvMgjahTWxYd_XFBI0KYZJaHUk1l1MhwgegnVgqXUGbYb7DNmGxEsuwcEcKbKBz9e5MNQayINWig9hTAD5eHvFRuEC7knIaO169ZErprdOkdMvq1R3gLWpyaLV-dUnBVgGFjIbeYsmdFSvoTOdMvSq9p5Gvr4myfyULiuUpZ5EAoD3kKYrdKfbt_-a588mMst8FAJJWkOi-4cJ7Pa52OtqzsQs31lDCAZmvdpzGYSG2w3AldQVQK1UpZm51dy3CFOAYsdi2BOJzrJgsUr6KLquPfSdQsaoZVmqYivEfdpxXHdKq2iNG8z4NoTUlZC89Ac7OHGsOnO6As258zSos0gonyTKoL123EUxmzDgItL285urGsoNe_0SFmM08bsfQvXAgpOBLONzNKIqZ90ofhOaFOu75cT1jy_WTPXpwcVfSmhJ3UWY0W9Qpn-k0q44183PEm5umFgVDLS516TaDVGTGeNHQG2gRbR6F6C7pe1C4psz8E4I8ira6aF4vCzFnbSEDbRehhIGs2zio_tPClr5GfRFN5LwZFYawLo-nXuf2tCD_uYe71Bg0zc-ez73BO56fFg4idxP2v99L3VEeYeugm7kDTxOof1-GhA'''
}

### 获取CMS上所有进行中的的素材实验方案
def get_imagegroup_from_CMS(address):
    url_prefixes = {
        "PBN": f"https://pbn-cms.learnings.ai/paint/v1/cms/abtest?limit=100&offset=0&country=",
        "ZC": f"https://zc-cms.learnings.ai/colorflow/v1/cms/abtest?offset=0&limit=50",
        "VC": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/abtest?offset=0&limit=50",
        "BP": f"https://bpbncms.idailybread.com/bpbn/v1/cms/abtest?limit=50&offset=0&status=0",
        "Vista": f"https://colorpad-cms.learnings.ai/colorpad/v1/cms/abtest?offset=0&limit=50",
    }
    address = address.split('_')[0]
    url = url_prefixes.get(address)
    try:
        response = session.get(url, headers=CMS_headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        if address.startswith("BP"):
            response_data = response.json()["data"]["content"]
        else:
            response_data = response.json()["data"]["list"]
        image_group = []
        for list in response_data:
            if address.startswith("BP") and list["status"] == 1:
                image_group.append(list["group_key"])
            elif not address.startswith("BP") and list["status"] == "ACTIVE":
                image_group.append(list["code"])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return set(image_group)

### 获取CMS上实验组中For you 未开启的方案：
def get_For_you_from_CMS():
    result_group = []
    grouplist = get_imagegroup_from_CMS("PBN")
    for group in grouplist:
        print(group)
        url = f"https://pbn-cms.learnings.ai/paint/v1/cms/abtest/{group}/category"
        try:
            response = session.get(url, headers=CMS_headers)
            response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
            response_data = response.json()["data"]["list"]
            for item in response_data:
                if item["id"] == "5fdb3cbf97428126950e5def" and item["show"] != False:
                    result_group.append(group)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
    return result_group
# print(get_For_you_from_CMS())

### 获取ABtest上所有进行中的的素材实验方案
def get_imagegroup_from_ABTest(address):
    APP_ID_iOS = {
        "PBN": "5b892d3a9f9b4e00011d1cf3",
        "ZC": "60385d8448b726000118051c",
        "VC": "64b4c18196b49d036a8d6bba",
        "BP": "5c00dc5713ab060001c19ea0",
        "Vista": "657953298aa0c540cc3fd85d"
    }
    APP_ID_Android = {
        "PBN": "5b84f58e689998000116d3fd",
        "ZC": "60385d6148b726000118051b",
        "VC": "64b4c17796b49d036a8d6bb9",
        "BP": "5bfb5a2b6ff9950001e9a969",
        "Vista": "657953298aa0c540cc3fd85d"  # 暂时使用iOS的补充一下
    }
    address = address.split('_')[0]
    url_iOS = f"https://api.learnings.ai/pm/abtest/v4.15/production/{APP_ID_iOS.get(address)}/params?version_code=0"
    url_Android = f"https://api.learnings.ai/pm/abtest/v4.15/production/{APP_ID_Android.get(address)}/params?version_code=0"
    url_list = [url_iOS, url_Android]
    image_group = []
    for url in url_list:
        try:
            response = session.get(url)
            response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
            response_data = response.json()["data"]["params"]
            # print(response_data)
            for list in response_data:
                if list["key"] == "imageGroupNum" or list["key"] == "image_test_v2" or list["key"] == "image_test_v3":
                    for value_list in list["value"]:
                        image_group.append(value_list["value"])
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
    if image_group == []:
        image_group.append("default")
    # print(set(image_group))
    return set(image_group)

### 对比CMS和ABtest的素材方案，获取最终需要测试的素材方案
def get_imagegroup(address):
    CMS_imagegroup = get_imagegroup_from_CMS(address)
    ABtest_imagegroup = get_imagegroup_from_ABTest(address)
    diff = ABtest_imagegroup.difference(set(CMS_imagegroup))
    if diff:
        raise Exception(f"List B contains data that is not in List A: {list(diff)}")
    else:
        return ABtest_imagegroup

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
    pic_id = []
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
        return pic_id
    elif address.startswith("PBN"):
        paintList = response_data["paintList"]
        for item in paintList:
            if item["releaseDate"] == formatted_date2:
                pic_id.append(item["id"])

    elif address.startswith(("VC", "ZC", "BP", "Vista")):
        content = response_data["content"]
        for detail_content in content:
            if (address in ["VC_Daily", "ZC_Daily", "Vista_Daily"] and detail_content["daily"] == formatted_date1) or \
                    (address in ["VC_Lib", "ZC_Lib", "Vista_Lib"] and detail_content["logic"]["release_date"] == formatted_date2):
                    pic_id.append(detail_content["detail"][0]["id"])

            elif (address in ["BP_Lib"] and detail_content["relase_date"] == formatted_date2) or \
                    (address in ["BP_Daily"] and str(detail_content["daily"]) == formatted_date2):  # 这里就是错误的relase_date拼写
                    pic_id.append(detail_content["id"])

    return pic_id

### 判断所有素材方案今天更新的素材是否一致，如果一致，则返回当天更新的素材数据
def get_all_imagegroup_pic_update(address):
    update_pic_id = []
    fail_group_list = []
    update_pic_id_group = []
    group_list = list(get_imagegroup(address))
    for group in group_list:
        update_pic_id = get_today_update_lib_or_daily_pic_data(address, limit=50, timezone=timezone, group=group)
        update_pic_id_group.append(len(update_pic_id))
    if all(x == update_pic_id_group[0] for x in update_pic_id_group):
        return update_pic_id, fail_group_list
    else:
        different_update_group = [i for i, x in enumerate(update_pic_id_group) if x != update_pic_id_group[0]]
        for number in different_update_group:
            fail_group = group_list[number]
            fail_group_list.append(fail_group)
            print("以下素材方案更新的素材数量有问题: ", str(fail_group_list))
        return update_pic_id, fail_group_list

### 获取PBN某个时区最新的故事线ID和里面的素材信息
def get_lastest_story_pic_id(time_zone):
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
    try:
        response = session.get(story_list_url, headers=headers_timezone)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        lastest_story_id = response.json()["data"][1]["newChallengeList"][0]["id"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return lastest_story_id

### 获取更新的故事线素材（通过对比0、8两个时区）
def get_today_uptate_story_pic_id():
    story_id_0 = get_lastest_story_pic_id(timezone)
    story_id_8 = get_lastest_story_pic_id(timezone_cn)
    if story_id_0 != story_id_8:
        print("今天上了新的故事线！")
        update_pid_id = story_id_0
    else:
        print("今天仅上了新的素材！")
        update_pid_id = [element for element in story_id_0 if element not in story_id_8]
    return update_pid_id

# 获取Vista某个时区最新3个的内购包里面的素材信息
def get_lastest_pack_pic_id(time_zone):
    pack_list_url = "https://colorpad-api.vitastudio.ai/colorpad/v1/paint/pack?limit=3"
    phone_headers = {
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
    lastest_pack_pic_id = []
    try:
        response = session.get(pack_list_url, headers=phone_headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        for data in response_data["content"]:
            paints = data["paints"]
            for paints_data in paints:
                lastest_pack_pic_id.append([paints_data["detail"][0]["id"]])
        return lastest_pack_pic_id
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 获取更新的内购包里面的素材id
def get_today_update_pack_pic_id():
    pack_pic_id_0 = get_lastest_pack_pic_id(timezone)
    pack_pic_id_8 = get_lastest_pack_pic_id(timezone_cn)
    update_pid_id = [element for element in pack_pic_id_0 if element not in pack_pic_id_8]
    return update_pid_id

# 判断所有方案内的所有素材内饰是否一致，不一致返回错误，一致返回今天的素材
def Check_image_group_pic_updata():
    ...

# 获取对应素材的zip包，解压并获得包内文件
def get_zip_detail(address, pic_id, zip_url):
    # 计算密码
    if address.startswith("BP"):
        pwd = "UHVnW2k9QWY3Smp2cGZIYldOdGt2eXZOcUt1dFQpOEY="
    else:
        # print(pic_id)
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
        # zf = zipfile.ZipFile(filename)
        zf = pyzipper.AESZipFile(filename, encryption=pyzipper.WZ_AES) ##加压zip更换了库，导致zipfile方法不可用
        zf.setpassword(pwd.encode())
        for name in zf.namelist():
            zf.extract(name, './%s/%s' % ("Pic", pic_id))
        zf.close()
    except zipfile.BadZipFile as e:
        print(f"文件损坏，无法解压: {e}")

