from Get_Pic import *
import PyPDF2
from PyPDF2 import errors
from Common_Fun import *

import pandas as pd
from collections import Counter

# 通过单素材详情接口获取Zip_url
def Get_id_Zipurl_from_picdetailapi(address,PicID):
    url_prefixes = {
        "PBN": f"https://paint-api.dailyinnovation.biz/paint/v1/paint/{PicID}",
        "ZC": f"https://api.colorflow.app/colorflow/v1/paint/{PicID}",
        "VC": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paint/{PicID}",
        "BP": f"https://bpbnapi.idailybread.com/paint/v1/paint/{PicID}",
        "Vista": f"https://colorpad-api.vitastudio.ai/colorpad/v1/paint/{PicID}"
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
    ids = []
    zip_url = []
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        if address == "PBN":
            if response_data["vector_zip_file"]:
                ids.append(PicID)
                zip_url.append(response_data["vector_zip_file"])
            else:
                ids.append(PicID)
                zip_url.append(response_data["zip_file"])
        elif address.startswith(("VC", "ZC", "Vista")):
            ids.append(PicID)
            zip_url.append(response_data["resource"]["zip"])
        elif address == "BP":
            ids.append(PicID)
            zip_url.append(response_data["zip_2048_pdf"])
        return ids, zip_url
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 从表格中读取数据作为素材数据
def get_picid_zipurl_from_excel(address):
    df = pd.read_excel('excel/test.xlsx', usecols=[0])
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

# 同时检测json和pdf资源
def Check_json_and_pdf(address):
    # ids, Zip_url = Get_id_Zipurl(address, limit=1000, group="c")  # 获取Lib、Daily要检测的素材信息：id、url

    ids, Zip_url = Get_id_Zipurl_from_picdetailapi(address, "65e965b27ba2388826a1ee55")  #检查单张素材
    # date = Get_Pack_Pic_Data("Pacific/Apia")    # 检查包素材
    # ids = [list(d.keys())[0] for d in date]  # 提取所有的键
    # Zip_url = [list(d.values())[0] for d in date]
    folder_path = '/Users/ht/Desktop/PythonTools/Pic_Check/Pic/' # zip资源下载路径，下载后自动清理
    failed_ids = []
    failed_ids_pdf = []
    failed_ids_number = []
    for ids_, Zip_url_ in zip(ids, Zip_url):
        print(ids_)
        data = Get_detailjson(ids_, Zip_url_, address)
        if Get_Number_From_Plan(data, address) == [] or Get_Number_From_Center(data) == []:
            failed_ids.append(ids_)
        elif set(Get_Number_From_Plan(data, address)) - set(Get_Number_From_Center(data)):
            failed_ids.append(ids_)
        if Get_Number_From_FloatCenter(data) != []:
            if set(Get_Number_From_Plan(data, address)) - set(Get_Number_From_FloatCenter(data)):
                failed_ids.append(ids_)
        pdf = Get_PDF(ids_, Zip_url_, address)
        if pdf:
            try:
                with open(pdf, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    if reader.is_encrypted:
                        continue
                    # 尝试读取PDF的每一页
                    for page in range(len(reader.pages)):
                        _ = reader.pages[page]  # 获取页面的方法也有变更
            except PyPDF2.errors.PdfReadError as e:  # 更新异常处理
                failed_ids_pdf.append(ids_)
            except OSError as e:  # OSError 保持不变
                failed_ids_pdf.append(ids_)
            if Check_Pdf_Block(pdf, ids_, Zip_url_, address) == False:
                failed_ids.append(ids_)
        if Test_area_and_FloatCenter(data) == False:
            failed_ids_number.append(ids_)
        # delete_folder(folder_path)
    print("*******test end********")
    print(failed_ids)
    print(failed_ids_pdf)
    print(failed_ids_number)

# Check_json_and_pdf("VC")
# Check_json_and_pdf("ZC_Daily")

# 检查素材PicID的json错误类型
def check_pic(address,PicID):
    id,Zip_url_ = Get_id_Zipurl_from_picdetailapi(address, PicID)
    data = Get_detailjson(id, Zip_url_, address)
    # print(Get_Number_From_Plan(data, address))
    # print(Get_Number_From_Center(data))
    # print(Get_Number_From_FloatCenter(data))
    if Get_Number_From_Plan(data, address) == [] or Get_Number_From_Center(data) == []:
        print("Get_Number_From_Plan/Get_Number_From_Center 为空")
    elif set(Get_Number_From_Plan(data, address)) - set(Get_Number_From_Center(data)):
        diff = set(Get_Number_From_Plan(data, address)) - set(Get_Number_From_Center(data))
        print("Get_Number_From_Plan - Get_Number_From_Center")
        print(diff)
    if Get_Number_From_FloatCenter(data) != []:
        if set(Get_Number_From_Plan(data, address)) - set(Get_Number_From_FloatCenter(data)):
            diff = set(Get_Number_From_Plan(data, address)) - set(Get_Number_From_FloatCenter(data))
            print("Get_Number_From_Plan - Get_Number_From_FloatCenter")
            print(diff)

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