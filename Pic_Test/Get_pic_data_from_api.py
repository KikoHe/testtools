from Get_zip_data import *
import pandas as pd
import json

# 通过单素材详情接口获取Zip_url
def Get_id_Zipurl_from_picdetailapi(PicID,address):
    url_prefixes = {
        "PBN": f"https://paint-api.dailyinnovation.biz/paint/v1/paint/{PicID}",
        "ZC": f"https://api.colorflow.app/colorflow/v1/paint/{PicID}",
        "VC": f"https://vitacolor-api.vitastudio.ai/vitacolor/v1/paint/{PicID}",
        "BP": f"https://bpbnapi.idailybread.com/paint/v1/paint/{PicID}",
        "Vista": f"https://colorpad-api.vitastudio.ai/colorpad/v1/paint/{PicID}"
    }
    headers = {
        "platform": "ios",
        "install_day": "100",
        "timezone": timezone,
        "today": formatted_date2,
        "country": "US",
        "version": "4.9.0",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "3488",
        # "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.4.10"
        "user-agent": "ios/17.5.1 com.paint.bynumber/4.12.0",
        "product-info": "ios/17.5.1 PBN/4.12.0 US",
        "support-blend": "true",
        "device-type": "phone"
    }
    url = url_prefixes.get(address.split('_')[0])
    svg_zip_url, not_svg_zip_url = '', ''
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        if address.startswith("PBN"):
            if response_data["vector_zip_file"]:
                not_svg_zip_url = response_data["vector_zip_file"]
            elif response_data["zip_file"]:
                not_svg_zip_url = response_data["zip_file"]
            if response_data["region_json_zip"]:
                svg_zip_url = response_data["region_json_zip"]
        elif address.startswith(("VC", "ZC", "Vista")):
            not_svg_zip_url = response_data["resource"]["zip"]
        elif address.startswith("BP"):
            not_svg_zip_url = response_data["zip_2048_pdf"]
        return not_svg_zip_url, svg_zip_url
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 获取CMS上素材方案配置内容：ID+data
def pic_config(address,offset=0,limit=100):
    url_prefixes = {
        "PBN": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?limit={limit}&offset={offset}&category_id=&authors=&color_type=&size_type=&tags=&with_preformance=false&status_list=&sort_by=c_time%5E-1&is_resource_update=IGNORE",
        "ZC": f"https://zc-cms.learnings.ai/colorflow/v1/cms/abtest/default/detail?limit={limit}&offset={offset}&release_date=2024-05-14%5E2024-05-14",
        "VC": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/abtest/default/detail?limit={limit}&offset={offset}&release_date=2024-05-01%5E2024-05-05",
        "BP": f"https://bpbncms.idailybread.com/bpbn/v1/cms/abtest/logic_item/test_a/list/trending?limit={limit}&offset={offset}&category_key=trending&size=&is_colored=false&is_gif=false&status=0&show_type=0&release_date_start=20240501&release_date_end=20240505&id_or_filename=&with_scores=true",
        "Vista": f"https://colorpad-cms.learnings.ai/colorpad/v1/cms/abtest/default/detail?limit={limit}&offset={offset}&release_date=2024-05-01%5E2024-05-05"
    }
    headers = {
        "cookie":'''_ga=GA1.1.1929480831.1691656939; learnings-passport=_sLoatJ7zrLmUuJjAyErLhekSW3RsYzZ2lr6_ZzTsiHgDHFKnnZS0taYmRszx8Wp; isArtist=false; projectIds=[%225b84f58e689998000116d3fd%22%2C%225b892d3a9f9b4e00011d1cf3%22%2C%225e43d79dbfe4170001141436%22]; products=[%225bfb5a2b6ff9950001e9a969%22%2C%225c00dc5713ab060001c19ea0%22%2C%225b18ef419c560300013ddf28%22%2C%225b18f0079c560300013ddf29%22%2C%225e43d79dbfe4170001141436%22%2C%225b84f58e689998000116d3fd%22%2C%225b892d3a9f9b4e00011d1cf3%22%2C%22657953298aa0c540cc3fd85d%22%2C%22655d7180648210324dccb499%22%2C%2264b4c17796b49d036a8d6bb9%22%2C%2264b4c18196b49d036a8d6bba%22%2C%22645b2f85cd911b5ea8511fd6%22%2C%2260385d6148b726000118051b%22%2C%2260385d8448b726000118051c%22]; ajs_anonymous_id=42cd20ca-c89e-49ac-ad60-eb63ead5252c; uac_passport="2|1:0|10:1719804699|12:uac_passport|44:ZjhjY2Y1Y2ZhYmVlNDA4ZjgyN2I0NzdhYzQwNDYyOWY=|07278d3a26be700c22ec6c25569b9c2fcea8b391ea5e95806372d99497d945d3"; _ga_2Z4PFG28RG=GS1.1.1719818527.767.1.1719818529.58.0.0; learnings-user=Y9TMYRYvMgjahTWxYd_XFBI0KYZJaHUk1l1MhwgegnVgqXUGbYb7DNmGxEsuwcEcKbKBz9e5MNQayINWig9hTAD5eHvFRuEC7knIaO169ZErprdOkdMvq1R3gLWpyaLV-dUnBVgGFjIbeYsmdFSvoTOdMvSq9p5Gvr4myfyULiuUpZ5EAoD3kKYrdKfbt_-a588mMst8FAJJWkOi-4cJ7Pa52OtqzsQs31lDCAZmvdpzGYSG2w3AldQVQK1UpZm51dy3CFOAYsdi2BOJzrJgsUr6KLquPfSdQsaoZVmqYivEfdpxXHdKq2iNG8z4NoTUlZC89Ac7OHGsOnO6As258zSos0gonyTKoL123EUxmzDgItL285urGsoNe_0SFmM08bsfQvXAgpOBLONzNKIqZ90ofhOaFOu75cT1jy_WTPXpwcVfSmhJ3UWY0W9Qpn-k0q44183PEm5umFgVDLS516TaDVGTGeNHQG2gRbR6F6C7pe1C4psz8E4I8ira6aF4vCzFnbSEDbRehhIGs2zio_tPClr5GfRFN5LwZFYawLo-nXuf2tCD_uYe71Bg0zc-ez73BO56fFg4idxP2v99L3VEeYeugm7kDTxOof1-GhA'''
    }
    url = url_prefixes.get(address)
    print(url)
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        if address == "PBN":
            response_data = response.json()["data"]["list"]
        else:
            response_data = response.json()["data"]["content"]
        # print(response_data)
        id_list = {}
        for list in response_data:
            if address == "PBN":
                id = list["id"]
                release_data = list["id"]
                # release_data = list["logic"]["ab_test_set"]["release_date"]
            elif address == "BP":
                id = list["paints"][0]["id"]
                release_data = list["release_date"]
            else:
                id = list["detail"][0]["id"]
                release_data = list["release_date"]
            id_list[id] = release_data
        return id_list
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 获取CMS上素材方案配置内容，并按照data返回素材张数
def Get_update_id_data(address):
    pic = pic_config(address)
    value_counts = {}
    # 遍历 id_list，统计每个 value 出现的次数
    for value in pic.values():
        if value in value_counts:
            value_counts[value] += 1
        else:
            value_counts[value] = 1
    # 打印每个 value 出现的次数
    for value, count in value_counts.items():
        print(f"{address} '{value}' 的素材张数: {count}")

def get_picid_from_excel(address, filename):
    df = pd.read_excel(filename, usecols=[0])
    data = df.to_dict(orient='split')
    json_data = {
        'columns': data['columns'],
        'data': data['data']
    }
    with open('excel/output.json', 'w') as f:
        json.dump(json_data, f)
    Pic_ids = []
    for data in json_data["data"]:
        pic_id = data[0]
        Pic_ids.append(pic_id)
    return Pic_ids

# 通过vincent获取素材area[未调通]
def get_area_from_vincent(pic_cms_id):
    area_data = {}
    area_number = []
    url_get_ma_id = f"https://vincent2.lexinshengwen.com/vincent/v1/material/manage?limit=50&offset=0&image_paint_from=&image_outside_painter=&demand_intermediary=&demand_audit_painter=&demand_content_painter=&demand_color_painter=&demand_line_painter=&demand=&demand_creator=&material=&fuzzy_search_numbers=&image=&cms_id={pic_cms_id}&image_paint_type=&image_size_type=&image_production_type=&demand_status=&demand_deadline_for_lining_start=&demand_deadline_for_lining_end=&demand_complete_time_start=&demand_complete_time_end=&demand_platform=&demand_module=&demand_category=&demand_tag=&material_platform=&material_module=&material_category=&demand_group=&demand_illustrator=&material_status="
    headers = {
        "Referrer Policy": "strict-origin-when-cross-origin",
        "Vincent_client_platform": "web",
        "Accept": '''application/json, text/plain, */*''',
        "Sec-Ch-Ua-Platform":"macOS",
        "Sec-Ch-Ua": '''"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"''',
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Cookie": '''_ga=GA1.1.1637196591.1691550110; uac_passport="2|1:0|10:1720665308|12:uac_passport|44:MGYxNmIxN2U5YjMyNDZjNGE4MDJhMWFkYTI0MWI4ZWU=|67111b814d055df4cddb02424e97b52b6ff73932b5c6b191abf4530e2e3dc388"; user="2|1:0|10:1720665308|4:user|696:eyJpZCI6ICI1Yzg1YzJlZDlkZWYyYzAwMDE2MzZjNGIiLCAidXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgIm9wZW5pZCI6ICJvdV9mNDgxNDBlNWNjM2NhY2ViYmIyZTQxMDM1NDYxMWM0OCIsICJuYW1lIjogIlx1NGY1NVx1NmQ5YiIsICJhdmF0YXIiOiAiaHR0cHM6Ly9zMS1pbWZpbGUuZmVpc2h1Y2RuLmNvbS9zdGF0aWMtcmVzb3VyY2UvdjEvdjJfOWFkY2YxOTAtNmI1Zi00MDAxLTgyY2UtMTI3OGMxYWI3ZTJnfj9pbWFnZV9zaXplPW5vb3AmY3V0X3R5cGU9JnF1YWxpdHk9JmZvcm1hdD1wbmcmc3RpY2tlcl9mb3JtYXQ9LndlYnAiLCAiZW1haWwiOiAiaGV0YW9AZGFpbHlpbm5vdmF0aW9uLmJpeiIsICJkZXBhcnRtZW50IjogWyJvZC0yYWZlZWZiMTJiMDM3MGMyZWI4YjAxOTY2ODhmN2IwOCJdLCAiYWN0aXZlIjogdHJ1ZSwgImpvYm51bWJlciI6ICIiLCAiZGluZ2RpbmdfdXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgImZlaXNodV91c2VyaWQiOiAiODMxMTQyZTUiLCAiaGlyZWQiOiAxOTUwfQ==|9cc4f3de99d494e209d7a00b381faed23032f5750fc54667f8ecc12b7ab7ef6b"; sidebarStatus=1; _ga_2Z4PFG28RG=GS1.1.1720686527.183.1.1720687409.39.0.0'''
    }
    try:
        response = session.get(url_get_ma_id, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        ma_id = response_data["demand_list"][0]["demand"]["material_list"][0]

        url = f"https://vincent2.lexinshengwen.com/vincent/v1/material/{ma_id}"
        response = session.get(url, headers=headers)
        response_data = response.json()["data"]
        area_data = response_data["image_list"][0]["coloring_list"][0]["area"]
        area_data = json.loads(area_data)
        area_number = list(area_data.keys())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return area_number, area_data
# print(get_area_from_vincent("65fd1c6a48defc641251e6f4"))

