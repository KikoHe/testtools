# 通过接口查询各个系统中素材的tag属性
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd

def get_url_headers(api_type, limit, offset):
    #枚举所有系统的数据接口url和headers
    if api_type == 'pbn':
        url = f'''https://pbn-cms-stage.learnings.ai/paint/v1/cms/paint?limit={limit}&offset={offset}&category_id=&authors=&color_type=&size_type=&tags=&with_preformance=false&status_list=&sort_by=c_time%5E-1&is_resource_update=IGNORE'''
        # url = f'''https://pbn-cms.learnings.ai/paint/v1/cms/paint?limit={limit}&offset={offset}&category_id=&authors=&color_type=&size_type=&tags=&with_preformance=false&status_list=&sort_by=c_time%5E-1&is_resource_update=IGNORE'''
        headers = {
            "Cookie": '''_ga=GA1.1.1929480831.1691656939; learnings-passport=EBH0lAfOxgQq90GrHPSdIFGaGgf_IGLhGWe1O53CoQOY8vKvW9nXHQZszwZauw20; learnings-user=lVeSR6Ly9Mm2BcY9X2kZPcdJG5oUkJx3OjFkNVJKB-cxD4xwsCdyWneh7Rhz0RZ29WkW1fX6vX3FsVtcTN2Nh34e9a2mde47LOtc6Wqdh1YhZW1ZLpD_BMYwsqRjN1FjUz-q0-fMDwPYpKEvE0h0I6O4d49Y81kvQtlO9lC-xGgk3n_bzXGeamh46nfCYIyfWvpuZtZbbnxQ8BmpTfSPFSCS1txNp7SC4pn_hfOC016BVwu4_s1IJ7_t5VXUnA05KVsoGt0AMH7NxPs_IJD6Sgt0rMA4ZH2R2T05D48RYNfztYsvYH14ut_LKxRsrK_PiT8KyJnOZVzhhKRi7JgZdrFO20qnOx0rakzG4pD1m7AKFYxkK6mufp-BPapGG_GG1fBO-lMFrZm9EuHCCPCTbPeB1x4Hxoob-uRybfpT-k23UlKotILiHKVR4fogWyejkmnP6Adw83W5Mip2_St3LyHTCVZvkPiJtmF-v2bHPclVk7k0U9o0CxOrkYUFsJ5TZWwPMC76zAMaMs79UZRE0JJl4KS5tNm65y1RyC62l5UXFvojbqPc1SbFLkzxQW1W3eAryvfkcfQA9atIbLggVP6TT9yjSRM7qE8rL8dqQZI; _ga_2Z4PFG28RG=GS1.1.1708481358.382.1.1708486541.60.0.0''',
            "Vincent_client_platform": "web"
        }
    elif api_type == 'vincent':
        # url = f'''https://vincent2.lexinshengwen.com/vincent/v1/material/global?limit={limit}&offset={offset}&image_paint_from=&image_outside_painter=&demand_intermediary=&demand_audit_painter=&demand_content_painter=&demand_color_painter=&demand_line_painter=&demand=&demand_creator=&material=&fuzzy_search_numbers=&image=&cms_id=&image_paint_type=&image_size_type=&image_production_type=&demand_status=&demand_deadline_for_lining_start=&demand_deadline_for_lining_end=&demand_complete_time_start=&demand_complete_time_end=&demand_platform=&demand_module=&demand_category=&demand_tag=&material_platform=ColorPad&material_module=&material_category=&material_tag=&demand_group=&demand_illustrator=&material_status='''
        url = f'''https://vincent2.lexinshengwen.com/vincent/v1/material/global?limit={limit}&offset={offset}&image_paint_from=&image_outside_painter=&demand_intermediary=&demand_audit_painter=&demand_content_painter=&demand_color_painter=&demand_line_painter=&demand=&demand_creator=&material=&fuzzy_search_numbers=&image=&cms_id=&image_paint_type=&image_size_type=&image_production_type=&demand_status=&demand_deadline_for_lining_start=&demand_deadline_for_lining_end=&demand_complete_time_start=&demand_complete_time_end=&demand_platform=&demand_module=&demand_category=&demand_tag=&material_platform=&material_module=&material_category=&demand_group=&demand_illustrator=&material_status='''
        headers = {
            "Cookie": '''_ga=GA1.1.1637196591.1691550110; sidebarStatus=0; uac_passport="2|1:0|10:1706665824|12:uac_passport|44:Yjg1N2QxNzZmNDk5NDdmZmIzMmI1YmYxNDUxZWE4YTk=|2f2fa92d8bdd58bb5597f615523e8ccf84f0a9f1de2f858ac18d62b911f04240"; user=2|1:0|10:1706665824|4:user|628:eyJpZCI6ICI1Yzg1YzJlZDlkZWYyYzAwMDE2MzZjNGIiLCAidXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgIm5hbWUiOiAiXHU0ZjU1XHU2ZDliIiwgImF2YXRhciI6ICJodHRwczovL3MxLWltZmlsZS5mZWlzaHVjZG4uY29tL3N0YXRpYy1yZXNvdXJjZS92MS92Ml85YWRjZjE5MC02YjVmLTQwMDEtODJjZS0xMjc4YzFhYjdlMmd+P2ltYWdlX3NpemU9bm9vcCZjdXRfdHlwZT0mcXVhbGl0eT0mZm9ybWF0PXBuZyZzdGlja2VyX2Zvcm1hdD0ud2VicCIsICJlbWFpbCI6ICJoZXRhb0BkYWlseWlubm92YXRpb24uYml6IiwgImRlcGFydG1lbnQiOiBbIm9kLTJhZmVlZmIxMmIwMzcwYzJlYjhiMDE5NjY4OGY3YjA4Il0sICJhY3RpdmUiOiB0cnVlLCAiam9ibnVtYmVyIjogIiIsICJkaW5nZGluZ191c2VyaWQiOiAiMTU1MjI2OTg3Nzc0OTYzODciLCAiZmVpc2h1X3VzZXJpZCI6ICI4MzExNDJlNSIsICJoaXJlZCI6IDE3ODh9|ac0f531d5cd072adac68610f1187677cf0605bc52b2e1093bb80a96cc7fab5cb; _ga_2Z4PFG28RG=GS1.1.1706665816.89.1.1706668018.59.0.0''',
            "Vincent_client_platform": "web"
        }
    elif api_type == "zc":
        url = f'''https://zc-cms-stage.learnings.ai/colorflow/v1/cms/paint?offset={offset}&limit={limit}'''
        # url = f'''https://zc-cms.learnings.ai/colorflow/v1/cms/paint?offset={offset}&limit={limit}'''
        headers = {
            "Cookie": '''_ga=GA1.1.1929480831.1691656939; name=%E4%BD%95%E6%B6%9B; avatar=https://s1-imfile.feishucdn.com/static-resource/v1/v2_9adcf190-6b5f-4001-82ce-1278c1ab7e2g~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp; id=5c85c2ed9def2c0001636c4b; learnings-passport=EBH0lAfOxgQq90GrHPSdIFGaGgf_IGLhGWe1O53CoQOY8vKvW9nXHQZszwZauw20; learnings-user=Z1-bVNSvI14NygsAWa_lRHgaeghMtZeezxxrou748bTSD_K9HFAvWIxZCutGOxDcSjF8TZHqlC0H0v1wL73guiD1PkxjYBDMQsfejUD-xcn8uiUmT1xW_JFbJVQKK4RqFg5tzCeqynz5hqA_U3lRJzX1TFgyCCjlzVzpKuYPJKcq7HKtkq5q4wE9IaUVN9A5XQ4sBjC1W52itnpoYlKxqDe2iHlIxptlekx2-mivj7i-lexgnkU1oJ5eJsjce2clMKGcYEfZUQmtvaja0rU0ypyXtbfdIu0wKujJm4xZo8wT5l2Vs1sAyYk7Igxqb5mRzyzkW-aBfvDHAxACDkM7XyjPvO9XRoQAR0a53kWCZUSc7TB3Zi24BChILnEtrPAXSfJwrEMsL83RQQdzFcKz_DwSO3Pmpvvmy2ZD3k0l95CoXgapQVhgrh8OupYveuAHgZYienI9a81mopuGbxpGinDuUSLG7ZM0GZoOasi2mjBVsNuZC6FMcz8314bYNdMmGmyiF4t3J2PQN7lWze1W_4dby0ddJr7r1GiZNlB9G3sg8T0cmSZVZotyk3I-TLyDnUPCS3F-0WjfMGybNgqZErO_Yw2jkuaqlnRCJlfE-Ok; _ga_2Z4PFG28RG=GS1.1.1708411797.379.1.1708419338.46.0.0''',
            "Vincent_client_platform": "web"
        }
    elif api_type == "vc":
        url = f'''https://vc-cms-stage.learnings.ai/vitacolor/v1/cms/paint?offset={offset}&limit={limit}'''
        # url = f'''https://vc-cms.learnings.ai/vitacolor/v1/cms/paint?offset={offset}&limit={limit}'''
        headers = {
            "Cookie": '''_ga=GA1.1.1929480831.1691656939; name=%E4%BD%95%E6%B6%9B; id=5c85c2ed9def2c0001636c4b; avatar=https://s1-imfile.feishucdn.com/static-resource/v1/v2_9adcf190-6b5f-4001-82ce-1278c1ab7e2g~?image_size=noop&cut_type=&quality=&format=png&sticker_format=.webp; learnings-passport=EBH0lAfOxgQq90GrHPSdIFGaGgf_IGLhGWe1O53CoQOY8vKvW9nXHQZszwZauw20; _ga_2Z4PFG28RG=GS1.1.1708411797.379.1.1708415957.60.0.0; learnings-user=bluifVYmgNIMsVszcHCd3A1maKLHIQnmUSU4MvWzxn9kkpnKskmX_0-zO5qMOpBfAsQ68O8HNWjh5ypfkYBh6MWDmD8tKiA39Gz_C-yluiRCKT2o_O7XFO2ZXRBPebv3yaDblxIJd4V5ldmbcg97koMY8OlZsyhDFAqxRGDBK9bfRWOjKKVmzEgrmWk2B_st4354XA9sKE-reRmOuVj7a0Ub7VYSrj0E2nh881jYZul1zSjarWGCOZCObD2lEhRNCH6piH-NwEuHEtkhmV7rmukIxkLOsBK5zIZj44ur6WZkA3m73oZG40D0dB2DMdf9ELeuAiob0pqLQi20NKKnTfMPG1CAxJhJSa84DxPkM_CM8y8X8-2wbkHc385TfTg389gEdHoatefaD3MaymYEaijZNB6oHzAqsUDiAyCV-tPUo55_tO_YWVhJX-IcoJgQ1wAwDP4RAf0JfYyaB3pGVUp5KFoNYwvp2tQE5NFf2iyZU42G9GdCLfCfqwkI9SNID8lp5z3XLAIqylmn9yU45LeEfhTzbcjg2vQV3US30ozGJS26Twi_W7Ywy12VQAS3A4LdQnHWpKfDB9cGyysSQlf5tnmCZ-2Q2Rq7-i0YZGk''',
            "Vincent_client_platform": "web"
        }
    elif api_type == "colorpad":
        url = f'''https://colorpad-cms-stage.learnings.ai/colorpad/v1/cms/paint?offset={offset}&limit={limit}'''
        # url = f'''https://colorpad-cms.learnings.ai/colorpad/v1/cms/paint?offset={offset}&limit={limit}'''
        headers = {
            "Cookie": '''_ga=GA1.1.1929480831.1691656939; learnings-passport=EBH0lAfOxgQq90GrHPSdIFGaGgf_IGLhGWe1O53CoQOY8vKvW9nXHQZszwZauw20; _ga_2Z4PFG28RG=GS1.1.1708506726.386.1.1708509274.9.0.0; learnings-user=Z1-bVNSvI14NygsAWa_lRHgaeghMtZeezxxrou748bTSD_K9HFAvWIxZCutGOxDcSjF8TZHqlC0H0v1wL73guiD1PkxjYBDMQsfejUD-xcn8uiUmT1xW_JFbJVQKK4RqFg5tzCeqynz5hqA_U3lRJzX1TFgyCCjlzVzpKuYPJKcq7HKtkq5q4wE9IaUVN9A5XQ4sBjC1W52itnpoYlKxqDe2iHlIxptlekx2-mivj7gpee_3Hc7EygiRn6OLMwo5YU1ng6cJSNKLifOCqDoT38_TTybLkBfntLJsyfLLxU9evH-1xcu6eEK7Nm2K-xJg5WMkISj6JWoMVmZ6aWAi8cZLTJJdKx690j-XXpVwDPBRnGdgplVgKWqryTDk_Hn3PRVWoKPnvOU_at0jmbtzHTyRI-qFcZ5mk7pRrAKLwOvHwMhs-cLaIzoKd4PqoqhzbsG_E-AlrIFoQntSahwgQcO1IKxtYOgMDgVPJ8rBhTHRln1lGrkSwJhDsIjyfse1l26wHsDwIqRMX5oidDTOjbckaid4F0r7HhJeXxSwox4tzfUNpoLa5VSQRsR7Jr1bw2dnDBXxA08Kg18gfrKNn1sHr-ut19DLdgT_1MSCEOo''',
            "Vincent_client_platform": "web"
        }
    else:
        raise ValueError("Invalid API type specified")
    return url, headers

def get_pic_info(project):
    #获取图片编号、cmsid、tag等信息
    limit = 100
    offset = 0
    first_write = True
    while True:
        pic_list, headers = get_url_headers(project, limit, offset)

        # 设置重试次数以及回退策略
        retries = Retry(total=5,  # 总尝试次数
                        backoff_factor=1,  # 回退等待时间的指数基数
                        status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

        # 创建一个带有重试的会话对象
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=retries))
        response = session.get(pic_list, headers=headers)
        results = []
        if project == "vincent":
            response_data = response.json()["data"]["demand_list"]
            if response_data == []:
                break
            for pic in response_data:
                if "number" in pic["image_list"][0]["material_list"][0]["material"]:
                    number = pic["image_list"][0]["material_list"][0]["material"]["number"]
                else:
                    number = pic["image_list"][0]["material_list"][0]["id"]
                    print(1)
                    print(number)
                status = pic["image_list"][0]["material_list"][0]["material"]["status"]
                cms_id = pic["image_list"][0]["material_list"][0]["cms"]["cms_id"]
                platform = pic["image_list"][0]["material_list"][0]["cms"]["platform"]
                operations_Tag_list = pic["image_list"][0]["material_list"][0]["cms"]["tag_list"]
                content_tag_list = pic["image_list"][0]["material_list"][0]["cms"]["content_tag_list"]
                if "supplement_tag_list" in pic["image_list"][0]["material_list"][0]["cms"]:
                    supplement_tag_list = pic["image_list"][0]["material_list"][0]["cms"]["supplement_tag_list"]
                else:
                    supplement_tag_list = None
                    print(2)
                    print(number)

                result_dict = {
                    "platform": platform,
                    "status": status,
                    "number": number,
                    "cms_id": cms_id,
                    "supplement_tag_list": supplement_tag_list,
                    "content_tag_list": content_tag_list,
                    "operations_tag_list": operations_Tag_list
                    }
                results.append(result_dict)
        elif project == "pbn":
            response_data = response.json()["data"]["list"]
            if response_data == []:
                break
            for pic in response_data:
                operations_Tag_list = pic["resource_logic"]["operation_tags"]
                content_tag_list = pic["resource_logic"]["content_tags"]
                supplement_tag_list = pic["resource_logic"]["supplement_tags"]
                cms_id = pic["id"]
                result_dict = {
                    "cms_id": cms_id,
                    "supplement_tag_list": supplement_tag_list,
                    "content_tag_list": content_tag_list,
                    "operations_tag_list": operations_Tag_list
                }
                results.append(result_dict)
        elif project == "zc"or project == "vc" or project == "colorpad":
            response_data = response.json()["data"]["paint_list"]
            if response_data == []:
                break
            for pic in response_data:
                operations_Tag_list = pic["detail"][0]["releation"]["operation_tag"]
                content_tag_list = pic["detail"][0]["releation"]["content_tag"]
                # supplement_tag_list = pic["detail"][0]["releation"]["supplement_tag"]
                cms_id = pic["detail"][0]["id"]
                result_dict = {
                    "cms_id": cms_id,
                    # "supplement_tag_list": supplement_tag_list,
                    "content_tag_list": content_tag_list,
                    "operations_tag_list": operations_Tag_list
                }
                results.append(result_dict)
        # 使用 pandas 创建 DataFrame
        df = pd.DataFrame(results)
        if first_write:
            df.to_csv(f'excel/{project}_after_refresh_data.csv', mode='w', index=False, header=True)
            first_write = False
        else:
            df.to_csv(f'excel/{project}_after_refresh_data.csv', mode='a', index=False, header=False)
        offset += limit
    print(f"Data exported successfully to {project}_data.csv")
# get_pic_info("zc")

def merge_table(project):
    # 基于ID合并两个表
    # 读取两个CSV文件
    df1 = pd.read_csv(f'excel/{project}_after_refresh_data.csv')
    df2 = pd.read_csv(f'excel/{project}_before_refresh_data.csv')
    # 基于ID合并两个DataFrame，这里以内连接为例
    merged_df = df1.merge(df2, on='cms_id', how='inner')  # 使用 'outer' 替换 'inner' 可进行外连接
    # 将合并后的DataFrame保存到新的CSV文件
    merged_df.to_csv(f'excel/{project}_merged_data.csv', index=False)
    print("The tables have been merged successfully and saved to merged_table.csv")
# merge_table("vc")

def compare_differences_tag(project):
    # 输出"两个列中内容不一样的素材"
    # 读取CSV文件到DataFrame
    df = pd.read_csv(f'excel/{project}_merged_data.csv')

    # 假设我们要比较的两个字段是'Column1'和'Column2'
    # 创建一个新的列'Difference'，这将是一个布尔列，显示两个字段是否不同
    df['Difference'] = df['operations_tag_list_x'] != df['operations_tag_list_y']

    # 添加额外的条件过滤，排除特定的差异组合
    excluded_combinations = [('生活环境的宁静', '宁静'), ('人工融入自然的宁静', '宁静'), ('魔法', '宁静'), ('禅意场所', '宁静'), ('美好生活的喜悦', '喜悦'), ('兴趣活动的喜悦', '兴趣'), ('美好事物带来的愉悦', '兴趣'), ('生机带来的希望', '运营Tag'), ('魔法', '奇幻'), ('探索外太空', '科幻'), ('经典童话再现', '童话'), ('拟人化', '其他幻想'), ('生机带来的希望', '秩序化实体'), ('自然与生态', '创意艺术'), ('生活与节日', '创意艺术'), ('现实想象创意', '创意艺术'), ('禅意主题创意', '创意艺术'),('美学风格', '古典艺术'), ('自然环境的宁静', '人工融入自然的宁静')]  # 添加需要排除的组合
    filter_condition = ~df.apply(lambda row: any(
        [(exclusion[0] in row['operations_tag_list_x'] and exclusion[1] in row['operations_tag_list_y']) for exclusion
         in excluded_combinations]), axis=1)
    df = df[filter_condition]

    # 筛选出有差异的数据行
    differences = df[df['Difference']]

    # 显示有差异的数据
    print(differences)

    # 如果需要，也可以将结果保存到新的 CSV 文件中
    differences.to_csv(f'excel/{project}_differences_data_clear.csv', index=False)
    # differences.to_csv(f'excel/{project}_differences_data_not_clear.csv', index=False)
# compare_differences_tag("vc")

def get_all_content_tag():
    # 设置重试次数以及回退策略
    retries = Retry(total=5,  # 总尝试次数
                    backoff_factor=1,  # 回退等待时间的指数基数
                    status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

    # 创建一个带有重试的会话对象
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))

    toppic_tag_id_list = ["60a395aa7a7db30339882e15","60a395aa7a7db30339882e1c","62bee081fdd4cdaf9ed8039a","60a395aa7a7db30339882e1a","62bee081fdd4cdaf9ed803f3","60a395aa7a7db30339882e14","60a395aa7a7db30339882e1b"]
    content_tag_list = []
    headers = {
        "Vincent_client_platform": "web",
        "cookie": '''_ga=GA1.1.1637196591.1691550110; sidebarStatus=1; uac_passport="2|1:0|10:1707129749|12:uac_passport|44:ZDZmNTM4YmRiOWQyNDJmOGI3MGZlZjI0ZDdiMmQ2YTU=|72f037e95f7938430607e70af50cbeab98b9c16be14541d1059b82b32c3b63d4"; user=2|1:0|10:1707129749|4:user|628:eyJpZCI6ICI1Yzg1YzJlZDlkZWYyYzAwMDE2MzZjNGIiLCAidXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgIm5hbWUiOiAiXHU0ZjU1XHU2ZDliIiwgImF2YXRhciI6ICJodHRwczovL3MxLWltZmlsZS5mZWlzaHVjZG4uY29tL3N0YXRpYy1yZXNvdXJjZS92MS92Ml85YWRjZjE5MC02YjVmLTQwMDEtODJjZS0xMjc4YzFhYjdlMmd+P2ltYWdlX3NpemU9bm9vcCZjdXRfdHlwZT0mcXVhbGl0eT0mZm9ybWF0PXBuZyZzdGlja2VyX2Zvcm1hdD0ud2VicCIsICJlbWFpbCI6ICJoZXRhb0BkYWlseWlubm92YXRpb24uYml6IiwgImRlcGFydG1lbnQiOiBbIm9kLTJhZmVlZmIxMmIwMzcwYzJlYjhiMDE5NjY4OGY3YjA4Il0sICJhY3RpdmUiOiB0cnVlLCAiam9ibnVtYmVyIjogIiIsICJkaW5nZGluZ191c2VyaWQiOiAiMTU1MjI2OTg3Nzc0OTYzODciLCAiZmVpc2h1X3VzZXJpZCI6ICI4MzExNDJlNSIsICJoaXJlZCI6IDE3OTN9|0d17a5b19415baa22957bf8f6c94866dc9eb6a5b887ed42a96843ec6ff9e3363; _ga_2Z4PFG28RG=GS1.1.1707129644.94.1.1707129781.49.0.0'''
    }
    for toppic_tag_id in toppic_tag_id_list:
        url = f"https://vincent2.lexinshengwen.com/vincent/v1/tag-group/content/{toppic_tag_id}?full_info=true"
        try:
            response = session.get(url, headers=headers)
            response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
            response_data = response.json()["data"]["tags"]
            for tags in response_data:
                content_tag = tags["name"]
                content_tag_list.append(content_tag)
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
    print(len(content_tag_list))
    return content_tag_list

def get_():
    # 读取 Excel 文件
    df = pd.read_csv('excel/differences1.csv')  # 替换为您的 Excel 文件路径
    # 定义集合 B
    set_b = get_all_content_tag()  # 替换为您的集合 B
    # 定义值 X 和 Y
    value_x = '大厅'  # 替换为您的值 X
    value_y = "生活环境的宁静1"  # 替换为您的值 Y
    print(set_b)

    for tag_content in df["content_tag_list_x"]:
        print(tag_content[' '])
        if tag_content in set_b:
            print(tag_content)

def test_pic_tag_refresh():
    refresh_rule = {

    }
    #PBNCMS正式环境header
    pbn_release_headers = {
        "Cookie": '''_ga=GA1.1.1637196591.1691550110; sidebarStatus=0; uac_passport="2|1:0|10:1706665824|12:uac_passport|44:Yjg1N2QxNzZmNDk5NDdmZmIzMmI1YmYxNDUxZWE4YTk=|2f2fa92d8bdd58bb5597f615523e8ccf84f0a9f1de2f858ac18d62b911f04240"; user=2|1:0|10:1706665824|4:user|628:eyJpZCI6ICI1Yzg1YzJlZDlkZWYyYzAwMDE2MzZjNGIiLCAidXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgIm5hbWUiOiAiXHU0ZjU1XHU2ZDliIiwgImF2YXRhciI6ICJodHRwczovL3MxLWltZmlsZS5mZWlzaHVjZG4uY29tL3N0YXRpYy1yZXNvdXJjZS92MS92Ml85YWRjZjE5MC02YjVmLTQwMDEtODJjZS0xMjc4YzFhYjdlMmd+P2ltYWdlX3NpemU9bm9vcCZjdXRfdHlwZT0mcXVhbGl0eT0mZm9ybWF0PXBuZyZzdGlja2VyX2Zvcm1hdD0ud2VicCIsICJlbWFpbCI6ICJoZXRhb0BkYWlseWlubm92YXRpb24uYml6IiwgImRlcGFydG1lbnQiOiBbIm9kLTJhZmVlZmIxMmIwMzcwYzJlYjhiMDE5NjY4OGY3YjA4Il0sICJhY3RpdmUiOiB0cnVlLCAiam9ibnVtYmVyIjogIiIsICJkaW5nZGluZ191c2VyaWQiOiAiMTU1MjI2OTg3Nzc0OTYzODciLCAiZmVpc2h1X3VzZXJpZCI6ICI4MzExNDJlNSIsICJoaXJlZCI6IDE3ODh9|ac0f531d5cd072adac68610f1187677cf0605bc52b2e1093bb80a96cc7fab5cb; _ga_2Z4PFG28RG=GS1.1.1706665816.89.1.1706668018.59.0.0''',
        "Vincent_client_platform": "web"
    }
    #PBNCMS正式环境请求接口，用来获取满足运营tag和内容tag 的所有素材
    pbn_release_piclist_for_tag_url = f'''https://pbn-cms.learnings.ai/paint/v1/cms/paint?limit=50&offset=0&category_id=&authors=&color_type=&size_type=&tags=&with_preformance=false&status_list=&sort_by=c_time%5E-1&operation_tags=%E5%AE%81%E9%9D%99&content_tags=%E5%85%B6%E4%BB%96%E7%8C%AB%5E%E5%96%9C%E9%A9%AC%E6%8B%89%E9%9B%85%E7%8C%AB%5E%E6%97%A0%E6%AF%9B%E7%8C%AB%5E%E6%A9%98%E7%8C%AB%5E%E5%B8%83%E5%81%B6%E7%8C%AB%5E%E8%8B%B1%E7%9F%AD%5E%E7%8B%B8%E8%8A%B1%E7%8C%AB%5E%E8%BE%B9%E5%A2%83%E7%89%A7%E7%BE%8A%E7%8A%AC%5E%E5%93%88%E5%A3%AB%E5%A5%87%5E%E6%9F%AF%E5%9F%BA%5E%E6%9F%B4%E7%8A%AC%5E%E8%B4%B5%E5%AE%BE%E7%8A%AC%5E%E9%87%91%E6%AF%9B%E7%8A%AC%5E%E5%BE%B7%E5%9B%BD%E7%89%A7%E7%BE%8A%E7%8A%AC%5E%E6%8B%89%E5%B8%83%E6%8B%89%E5%A4%9A%E7%8A%AC%5E%E5%85%B6%E4%BB%96%E7%8B%97%5E%E6%96%91%E7%82%B9%E7%8A%AC%5E%E8%97%8F%E7%8D%92%E7%8A%AC%5E%E5%8F%B2%E5%AE%BE%E6%A0%BC%E7%8A%AC%5E%E6%96%97%E7%89%9B%E7%8A%AC%5E%E5%90%89%E5%A8%83%E5%A8%83%E7%8A%AC%5E%E5%8D%9A%E7%BE%8E%E7%8A%AC%5E%E5%A4%9A%E7%A7%8D%E5%AE%A0%E7%89%A9&is_resource_update=IGNORE'''


    # vincent测式环境header，刷新后的数据在这里
    vincent_debug_headers = {
        "Cookie": '''_ga=GA1.1.1637196591.1691550110; sidebarStatus=0; uac_passport="2|1:0|10:1706665824|12:uac_passport|44:Yjg1N2QxNzZmNDk5NDdmZmIzMmI1YmYxNDUxZWE4YTk=|2f2fa92d8bdd58bb5597f615523e8ccf84f0a9f1de2f858ac18d62b911f04240"; user=2|1:0|10:1706665824|4:user|628:eyJpZCI6ICI1Yzg1YzJlZDlkZWYyYzAwMDE2MzZjNGIiLCAidXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgIm5hbWUiOiAiXHU0ZjU1XHU2ZDliIiwgImF2YXRhciI6ICJodHRwczovL3MxLWltZmlsZS5mZWlzaHVjZG4uY29tL3N0YXRpYy1yZXNvdXJjZS92MS92Ml85YWRjZjE5MC02YjVmLTQwMDEtODJjZS0xMjc4YzFhYjdlMmd+P2ltYWdlX3NpemU9bm9vcCZjdXRfdHlwZT0mcXVhbGl0eT0mZm9ybWF0PXBuZyZzdGlja2VyX2Zvcm1hdD0ud2VicCIsICJlbWFpbCI6ICJoZXRhb0BkYWlseWlubm92YXRpb24uYml6IiwgImRlcGFydG1lbnQiOiBbIm9kLTJhZmVlZmIxMmIwMzcwYzJlYjhiMDE5NjY4OGY3YjA4Il0sICJhY3RpdmUiOiB0cnVlLCAiam9ibnVtYmVyIjogIiIsICJkaW5nZGluZ191c2VyaWQiOiAiMTU1MjI2OTg3Nzc0OTYzODciLCAiZmVpc2h1X3VzZXJpZCI6ICI4MzExNDJlNSIsICJoaXJlZCI6IDE3ODh9|ac0f531d5cd072adac68610f1187677cf0605bc52b2e1093bb80a96cc7fab5cb; _ga_2Z4PFG28RG=GS1.1.1706665816.89.1.1706668018.59.0.0''',
        "Vincent_client_platform": "web"
    }
    # 获取到满足运营tag和内容tag的所有素材后，查看这些刷新后的素材的运营tag是否满足预期映射关系
    vincent_debug_picinfo_url = f''''''