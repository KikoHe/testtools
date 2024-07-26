import logging
from Public_env import *
from Get_pic_data_from_api import *

# 通过单素材详情接口获取Zip_url
# PicID:图片ID
# address：项目代码
def Get_id_Zipurl_from_picdetailapi(PicID,address):
    url_prefixes = {
        "PBN": f"https://paint-api.dailyinnovation.biz/paint/v1/paint/{PicID}",
        # "PBN": f"https://paint-api-stage.dailyinnovation.biz/paint/v1/paint/{PicID}",
        "ZC": f"https://api.colorflow.app/colorflow/v1/paint/{PicID}",
        "VC": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paint/{PicID}",
        "BP": f"https://bpbnapi.idailybread.com/paint/v1/paint/{PicID}",
        "Vista": f"https://colorpad-api.vitastudio.ai/colorpad/v1/paint/{PicID}"
    }
    url = url_prefixes.get(address.split('_')[0])
    svg_zip_url, pdf_zip_url, vector_zip_url = '', '', ''
    try:
        response = session.get(url, headers=phone_headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        if address.startswith("PBN"):
            if response_data["zip_file"]:
                pdf_zip_url = response_data["zip_file"]
            if response_data["vector_zip_file"]:
                vector_zip_url = response_data["vector_zip_file"]
            if response_data["region_json_zip"]:
                svg_zip_url = response_data["region_json_zip"]
        elif address.startswith(("VC", "ZC", "Vista")):
            pdf_zip_url = response_data["resource"]["zip"]
        elif address.startswith("BP"):
            pdf_zip_url = response_data["zip_2048_pdf"]
        return pdf_zip_url, vector_zip_url, svg_zip_url
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

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
            for list in response_data:
                if list["key"] == "imageGroupNum" or list["key"] == "image_test_v2" or list["key"] == "image_test_v3":
                    for value_list in list["value"]:
                        image_group.append(value_list["value"])
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
    if image_group == []:
        image_group.append("default")
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
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    if response_data == {}:
        logging.info("列表数据请求失败： "+str(url)+str(headers))
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
            logging.error("以下素材方案更新的素材数量有问题: ", str(fail_group_list))
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
    lastest_story_id, lastest_story_id_pic_id = [], []
    try:
        response = session.get(story_list_url, headers=headers_timezone)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        lastest_story_id = response.json()["data"][1]["newChallengeList"][0]["id"]
        lastest_story_id_pic_id = response.json()["data"][1]["newChallengeList"][0]["paintIdList"]
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
    return lastest_story_id, lastest_story_id_pic_id

### 获取更新的故事线素材（通过对比0、8两个时区）
def get_today_uptate_story_pic_id():
    story_id_0, pic_id_0 = get_lastest_story_pic_id(timezone)
    story_id_8, pic_id_8 = get_lastest_story_pic_id(timezone_cn)
    if story_id_0 != story_id_8:
        logging.info("今天上了新的故事线！")
        update_pid_id = pic_id_0
    else:
        update_pid_id = [element for element in pic_id_0 if element not in pic_id_8]
    return update_pid_id

# 获取Vista某个时区最新3个的内购包里面的素材信息
def get_lastest_pack_pic_id(time_zone):
    pack_list_url = "https://colorpad-api.vitastudio.ai/colorpad/v1/paint/pack?limit=3"
    headers_timezone = {
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
        response = session.get(pack_list_url, headers=headers_timezone)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        for data in response_data["content"]:
            paints = data["paints"]
            for paints_data in paints:
                lastest_pack_pic_id.append(paints_data["detail"][0]["id"])
        return lastest_pack_pic_id
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

# 获取更新的内购包里面的素材id
def get_today_update_pack_pic_id():
    pack_pic_id_0 = get_lastest_pack_pic_id(timezone)
    pack_pic_id_8 = get_lastest_pack_pic_id(timezone_cn)
    update_pid_id = [element for element in pack_pic_id_0 if element not in pack_pic_id_8]
    return update_pid_id

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
        logging.error(f"请求ZIP包时发生错误: {e}")
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
        logging.error(f"文件损坏，无法解压: {e}")