import json,pytz,hashlib, zipfile,os,requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
from collections import Counter

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
def Get_List(address, limit=10, timezone=timezone):
    url_prefixes = {
        "ZC_Lib": f"https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?limit={limit}",
        "ZC_Daily": f"https://api.colorflow.app/colorflow/v1/daily?query_date={formatted_date1}",
        "VC_Lib": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paintcategory/all/paints?limit={limit}",
        "VC_Daily": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/daily?query_date={formatted_date1}",
        "PBN_Lib": f"https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5ba31d31fe401a000102966e/paints?day=100&limit={limit}",
        "PBN_Daily": f"https://paint-api.dailyinnovation.biz/paint/v1/daily?groupNumber=c&day=0&limit=400&offset=0",
        "BP_Lib": f"https://bpbnapi.idailybread.com/paint/v1/paintCategory/trending/list?limit={limit}&offset=0&day=502&group_key=test_a&isAddDayMax=false&read_unactive=false&time_date=1703746118589&sort_plan=normal",
        "BP_Daily": f"https://bpbnapi.idailybread.com/paint/v1/daily/{formatted_date3}",
        "Vista_Lib": f"https://colorpad-api.vitastudio.ai/colorpad/v1/paintcategory/all/paints?offset=0&limit={limit}",
        "Vista_Daily": f"https://colorpad-api.vitastudio.ai/colorpad/v1/daily?query_date={formatted_date1}"
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

# 获取Get_List列表数据中图片ID和zip包url
def Get_id_Zipurl(address, limit):
    Pic_ids = []
    Zip_url = []
    attempt_count = 0
    while True:
        data = Get_List(address, limit)
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
            break
    return Pic_ids, Zip_url


# 获取不同时区最新的故事线ID
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

# 获取不同时区最新故事线的素材ID
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

# 获取更新的故事素材ID和url
def Get_stroyupdatepicid():
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
            print("No center_float" )
    return sorted(center_number_code_list)

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
        plan_number = plan[0].split('|')  # 色号数
        # sehaobianhao  = 1
        for i in range(len(plan_number)):
            plan_number_code = plan_number[i].split('#')[0].split(',')
            for num in range(len(plan_number_code)):
                plan_number_code_single = plan_number_code[num - 1]
                plan_number_code_int = int(plan_number_code_single)
                # if plan_number_code_int == 1039:
                #     print(sehaobianhao)
                plan_number_code_list.insert(-1, plan_number_code_int)
            # sehaobianhao = sehaobianhao +1
    return sorted(plan_number_code_list)

# 通过单素材详情接口获取zip url
def Get_id_Zipurl_from_picdetailapi(PicID,address):
    url_prefixes = {
        "PBN": f"https://paint-api.dailyinnovation.biz/paint/v1/paint/{PicID}",
        "ZC":f"https://api.colorflow.app/colorflow/v1/paint/{PicID}",
        "VC":f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paint/{PicID}",
        "BP":f"https://bpbnapi.idailybread.com/paint/v1/paint/{PicID}"
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
        if address == "PBN":
            if response_data["vector_zip_file"]:
                return(PicID,response_data["vector_zip_file"])
            else:
                return(PicID,response_data["zip_file"])
        elif address.startswith(("VC", "ZC")):
            return (PicID,response_data["resource"]["zip"])
        elif address == "BP":
            return(PicID, response_data["zip_2048_pdf"])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 获取excel表中素材ID的zip url
def get_picid_zipurl_from_excel(address):
    df = pd.read_excel('excel/12121test.xlsx', usecols=[0])
    data = df.to_dict(orient='split')
    json_data = {
        'columns': data['columns'],
        'data': data['data']
    }
    with open('excel/output.json', 'w') as f:
        json.dump(json_data, f)
    Pic_ids = []
    Zip_url = []
    for data in json_data["data"]:
        pic_id = data[0]
        picid, zipurl = Get_id_Zipurl_from_picdetailapi(pic_id, address)
        Pic_ids.append(picid)
        Zip_url.append(zipurl)
    return Pic_ids, Zip_url

# 检查素材在CMS上的配置
def pic_config(address):
    url_prefixes = {
        "PBN": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?abtest_key=c&limit=500&offset=0&status_list=ONLINE_LIBRARY&paint_id=&abtest_show=true&u_time_range=20240205_20240229&category_id=&with_userscore=true&sort_by=release_date%5E-1",
        # "ZC": f"https://zc-cms.learnings.ai/colorflow/v1/cms/daily?limit=200&offset=0&release_date=2024-02-05~2024-03-01",
        "ZC": f"https://zc-cms.learnings.ai/colorflow/v1/cms/abtest/default/detail?limit=500&offset=0&release_date=2024-02-05%5E2024-02-29",
        "VC": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/abtest/default/detail?limit=500&offset=0&release_date=2024-02-05%5E2024-02-29",
        "BP": f"https://bpbncms.idailybread.com/bpbn/v1/cms/daily?date_start=20240205&date_end=20240229&limit=200&offset=0"
    }
    headers = {
        # "cookie":"_ga=GA1.1.1929480831.1691656939; isArtist=false; learnings-passport=EBH0lAfOxgQq90GrHPSdIFGaGgf_IGLhGWe1O53CoQOY8vKvW9nXHQZszwZauw20; learnings-user=jOtSLUDcxz0Rqm5CFl0wv3vUKHxw4hfPXySdC0tteGjdSuzc2S9dWSscm6EpMnrgmvlxo3MtKJDSL2QRR2lDHoWoQanLZojxDmybNMWODWJKrELGFwmAbGG_08mYaJ9ytZyQWz2zuVDa6n6KhihlNLbbZ-w4c6Q9Ao7JR7dEV9C6mwrpeJO-vVinPyD_YBL0AO_0f7sYs_XMbX7_qBCTAbwSOPA50gDjk9MeThQLcVheB4qjwFbHkflc-nkzofL38Q8lw2vEE4uFRkCViCL6GfVuLLO6vrTfAbpPP4_5p5cBtiAvTJVMtPae-A7hT73fE-lvx-TG6uGBTyC2KJ3RpZg3jhEkZStqRD2WQMRfRhzousFONxgPK0Tk04InttOXUobw926QK5PIpUoFOlFNu0SdXHsCz-aIIcgWG39MmXCmIA4ZdsgoFbk7Z071lYzbMnXrbeYlFo_LfDzAtJnSH7B7jeJW-a2ZmTzsCjeLMBMAS1uM31gnRP1hKTT9OWZTlEVM6GdjGbgfvs6mYb_evgDofEiF0p1Q-Lga6W20RTNkFLij_vDvcDRfzmzXMOMozMYa680odUYfKjWL_v4kT_ATCTTYJE4zSyHBPzT3ThQ; _ga_2Z4PFG28RG=GS1.1.1707124810.358.1.1707124832.38.0.0"
        "cookie":"_ga=GA1.1.1929480831.1691656939; name=%E4%BD%95%E6%B6%9B; avatar=https://s1-imfile.feishucdn.com/static-resource/v1/v2_9adcf190-6b5f-4001-82ce-1278c1ab7e2g~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp; id=5c85c2ed9def2c0001636c4b; learnings-passport=EBH0lAfOxgQq90GrHPSdIFGaGgf_IGLhGWe1O53CoQOY8vKvW9nXHQZszwZauw20; learnings-user=Z1-bVNSvI14NygsAWa_lRHgaeghMtZeezxxrou748bTSD_K9HFAvWIxZCutGOxDcSjF8TZHqlC0H0v1wL73guiD1PkxjYBDMQsfejUD-xcn8uiUmT1xW_JFbJVQKK4RqFg5tzCeqynz5hqA_U3lRJzX1TFgyCCjlzVzpKuYPJKcq7HKtkq5q4wE9IaUVN9A5XQ4sBjC1W52itnpoYlKxqDe2iHlIxptlekx2-mivj7ghoD5b0RMFEeiguN-S80pLsBFfYmZ9O91PSbo-e9Ufr2hO140KoB1SP0btGCLz_NsFUEuI7kmsKjCqWhYJxHqqe2KUhVTPU0pQKYEQkD_TmHb-ty0u9AkIU561k2QL40SAlhLiSK9b0piZ7Ce-gP_HukkXLXYQrPLiMI5PZ2-vJYBphsctwCgm0wdR3qPTFmmhyB2x8ZiyfL4pYq_Vt0sgyMvYnzgo4d_b7hRs_DAndgrur2zi9gbsrsHpfrwrqGu2Uc0wgwJuzcB0iynkNUXngsI5US1IHw5oqOCi6OlRbFoDdkLiG1D9jKXHJgS6wV5T9Jid45FZrBi06hXuVGaFihrfJmP4zMDvBZhA89fNeirkatm25J6qXvCE4BRwQeo; _ga_2Z4PFG28RG=GS1.1.1707186605.362.1.1707186606.59.0.0"
        # "cookie":"_ga=GA1.1.1929480831.1691656939; name=%E4%BD%95%E6%B6%9B; id=5c85c2ed9def2c0001636c4b; avatar=https://s1-imfile.feishucdn.com/static-resource/v1/v2_9adcf190-6b5f-4001-82ce-1278c1ab7e2g~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp; learnings-passport=EBH0lAfOxgQq90GrHPSdIFGaGgf_IGLhGWe1O53CoQOY8vKvW9nXHQZszwZauw20; learnings-user=Ou7DP0e3gj7hKCv6Vp_u07qL8XuAbzmZtA2imbFJ69_G7PgF_8m1kJVQE_vZ6FDplIzaRJ86YeTM3L8mpmqQZlpXsUIaSAZVxTbJ09gtiHYbqC-A21l788of_99X8TRKoNAA8t3DDFCBkkqP6dNclMWBbIioTCuA3M9YZrUePWSPE9s0z4xJgExt6svjIcYX89Pp_uu2khmZbK2d-3poNEx7FtclZR2HrNILYeUWfUBRoOANdbbTYCfBsiodp2zJ338mH55PVqs9bdPZQZvzvb-To-wAPKgpMnXfun4FVr7uOfgpgh6gwsDWrmMBJEIpWQqKRBW075C-15NQckngxZIlliffaaBuFILF5sPOOwlLRnNgFxKztY0KXvpJlVVQALkifC7bnmi7v3H6V76-kgxRHaeBVREvU0Nl1VyKNdrmdXndZgp3jAWFr8HkQLQoqV2uP06U9LhGEDAgLiV0Y4DG5Jw2pIdgWdmJBKNR6KTIQJUY2GZA_aFpGRP1oaYTNrxGrZQ48yBhVoja7OffcrTzSRBKjfCe7Sm10hdaL0aVF5OAUnvMZEA2AT7W0g9fJv2LcVDU0QeycrvPEyy8x02SYNIcYGlOPmhgREDUzu8; _ga_2Z4PFG28RG=GS1.1.1707124810.358.1.1707126342.42.0.0"
        # "cookie": '''_ga=GA1.1.1084550949.1697188455; uac_passport="2|1:0|10:1707126693|12:uac_passport|44:YmM4MTA5N2UzMjI4NDIzYzkwZmExYjc3ODFlYjUwMzE=|a25a884a0f84140b1310aed889f795ee65373c6e29c5a8b0b4178139492fe9af"; user="2|1:0|10:1707126693|4:user|608:eyJpZCI6IjVjODVjMmVkOWRlZjJjMDAwMTYzNmM0YiIsInVzZXJpZCI6IjE1NTIyNjk4Nzc3NDk2Mzg3IiwibmFtZSI6Ilx1NGY1NVx1NmQ5YiIsImF2YXRhciI6Imh0dHBzOlwvXC9zMS1pbWZpbGUuZmVpc2h1Y2RuLmNvbVwvc3RhdGljLXJlc291cmNlXC92MVwvdjJfOWFkY2YxOTAtNmI1Zi00MDAxLTgyY2UtMTI3OGMxYWI3ZTJnfj9pbWFnZV9zaXplPW5vb3AmY3V0X3R5cGU9JnF1YWxpdHk9JmZvcm1hdD1wbmcmc3RpY2tlcl9mb3JtYXQ9LndlYnAiLCJlbWFpbCI6ImhldGFvQGRhaWx5aW5ub3ZhdGlvbi5iaXoiLCJkZXBhcnRtZW50IjpbIm9kLTJhZmVlZmIxMmIwMzcwYzJlYjhiMDE5NjY4OGY3YjA4Il0sImFjdGl2ZSI6dHJ1ZSwiam9ibnVtYmVyIjoiIiwiZGluZ2RpbmdfdXNlcmlkIjoiMTU1MjI2OTg3Nzc0OTYzODciLCJmZWlzaHVfdXNlcmlkIjoiODMxMTQyZTUiLCJoaXJlZCI6MTc5M30=|e051a7b239d5f9e9cda34ad4da2c84b52cf69b0ac14deb3ab5073b1b7aae24ab"; _ga_2Z4PFG28RG=GS1.1.1707126686.13.1.1707126725.21.0.0'''
    }
    url = url_prefixes.get(address)
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        # response_data = response.json()["data"]["list"]
        response_data = response.json()["data"]["content"]
        id_list = []
        for list in response_data:
            # id = list["id"]
            # release_data = list["logic"]["ab_test_set"]["release_date"]
            # release_data = list["logic"]["daily_set"]["daily"]
            release_data = list["release_date"]
            # release_data = list["daily"]
            id_list.append(release_data)
        counter = Counter(id_list)
        for element, count in counter.items():
            print(f"{element}: {count}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")