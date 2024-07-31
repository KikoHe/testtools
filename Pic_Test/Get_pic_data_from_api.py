import json
import logging

from Get_zip_data import *
import pandas as pd
from Public_env import *

# 获取CMS上所有进行中的的素材实验方案
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
    image_group = []
    try:
        response = session.get(url, headers=CMS_headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        if address.startswith("BP"):
            response_data = response.json()["data"]["content"]
        else:
            response_data = response.json()["data"]["list"]
        for list in response_data:
            if address.startswith("BP") and list["status"] == 1:
                image_group.append(list["group_key"])
            elif not address.startswith("BP") and list["status"] == "ACTIVE":
                image_group.append(list["code"])

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")
    return set(image_group)

# 获取CMS上所有进行中素材方案中For you分类未开启的方案：
def get_For_you_from_CMS():
    result_group = []
    grouplist = get_imagegroup_from_CMS("PBN")
    for group in grouplist:
        logging.info("group: %s", group)
        url = f"https://pbn-cms.learnings.ai/paint/v1/cms/abtest/{group}/category"
        try:
            response = session.get(url, headers=CMS_headers)
            response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
            response_data = response.json()["data"]["list"]
            for item in response_data:
                if item["id"] == "5fdb3cbf97428126950e5def" and item["show"] != False:
                    result_group.append(group)
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")
    return result_group

# 获取CMS上全局素材库的所有素材ID
def get_all_picid_from_cms(address,offset=0,limit=100):
    url_prefixes = {
        "PBN": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?limit={limit}&offset={offset}&category_id=&authors=&color_type=&size_type=&tags=&with_preformance=false&status_list=&sort_by=c_time%5E-1&is_resource_update=IGNORE",
        "ZC": f"https://zc-cms.learnings.ai/colorflow/v1/cms/abtest/default/detail?limit={limit}&offset={offset}",
        "VC": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/abtest/default/detail?limit={limit}&offset={offset}",
        "Vista": f"https://colorpad-cms.learnings.ai/colorpad/v1/cms/abtest/default/detail?limit={limit}&offset={offset}",
        "BP": f"https://bpbncms.idailybread.com/bpbn/v1/cms/abtest/logic_item/test_a/list/trending?limit={limit}&offset={offset}&category_key=trending&size=&is_colored=false&is_gif=false&status=0&show_type=0&id_or_filename=&with_scores=true"
    }
    print(address)
    url = url_prefixes.get(address)
    logging.info("CMS_url: %s", url)
    try:
        response = session.get(url, headers=CMS_headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        if address == "PBN":
            response_data = response.json()["data"]["list"]
        else:
            response_data = response.json()["data"]["content"]
        id_list = []
        for item in response_data:
            if address == "PBN":
                id_list.append(item["id"])
            elif address == "BP":
                id_list.append(item["paints"][0]["id"])
            else:
                id_list.append(item["detail"][0]["id"])
        return id_list
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An error occurred: {err}")

# 获取CMS上素材方案中某天的运营素材
# test_day：X天
def get_release_day_picid_from_cms(address, test_day=today):
    if address in ["BP_Lib", "BP_Daily"]:
        test_day = test_day.strftime("%Y%m%d")
    else:
        test_day = test_day.strftime("%Y-%m-%d")
    url_prefixes = {
        "PBN_Lib": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?abtest_key=default&limit=1000&offset=0&status_list=ONLINE_LIBRARY&abtest_release_date_range={test_day}T00:00:00_{test_day}T00:00:00&paint_id=&abtest_show=true&category_id=&with_userscore=true&sort_by=release_date%5E-1",
        "PBN_Daily": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?abtest_key=default&limit=50&offset=0&status_list=ONLINE_DAILY&abtest_daily_range={test_day}T00:00:00_{test_day}T00:00:00&paint_id=&abtest_show=true&sort_by=daily%5E-1",
        "VC_Lib": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/abtest/default/details",
        "VC_Daily": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/dailys",
        "ZC_Lib": f"https://zc-cms.learnings.ai/colorflow/v1/cms/abtest/default/details",
        "ZC_Daily": f"https://zc-cms.learnings.ai/colorflow/v1/cms/dailys",
        "Vista_Lib": f"https://colorpad-cms.learnings.ai/colorpad/v1/cms/abtest/default/details",
        "Vista_Daily": f"https://colorpad-cms.learnings.ai/colorpad/v1/cms/dailys",
        "BP_Lib": f"https://bpbncms.idailybread.com/bpbn/v1/cms/abtest/logic_item/default/list/trending?limit=20&offset=0&category_key=trending&size=&is_colored=false&is_gif=false&status=0&show_type=0&release_date_start={test_day}&release_date_end={test_day}&id_or_filename=&with_scores=true",
        "BP_Daily": f"https://bpbncms.idailybread.com/bpbn/v1/cms/daily?date_start={test_day}&date_end={test_day}&limit=200&offset=0"
    }
    payload_lib = {"limit": 50, "offset": 0, "release_date": f"{test_day}^{test_day}"}
    payload_daily = {"limit": 50, "offset": 0, "release_date": f"{test_day}~{test_day}"}
    url = url_prefixes.get(address)
    logging.info("CMS_url: %s", url)
    response = {}
    try:
        if address in ["PBN_Lib", "BP_Lib", "PBN_Daily", "BP_Daily"]:
            response = session.get(url, headers=CMS_headers)
        elif address in ["ZC_Daily", "VC_Daily", "Vista_Daily"]:
            response = session.post(url, headers=CMS_headers, json=payload_daily)
        else:
            response = session.post(url, headers=CMS_headers, json=payload_lib)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        print(response.text)
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    if address in ["PBN_Lib", "PBN_Daily"]:
        response_data = response.json()["data"]["list"]
    else:
        response_data = response.json()["data"]["content"]

    id_list = []
    for item in response_data:
        if address in ["PBN_Lib", "PBN_Daily"]:
            id_list.append(item["id"])
        elif address in ["BP_Lib"]:
            id_list.append(item["paints"][0]["id"])
        elif address in ["BP_Daily"]:
            id_list.append(item["id"])
        else:
            id_list.append(item["detail"][0]["id"])
    return id_list

# 检查素材方案的配置内容
def check_CMS_pic_config(group_id='',address='PBN_Lib', test_day=today):
    if address in ["BP_Lib", "BP_Daily"]:
        test_day = test_day.strftime("%Y%m%d")
    else:
        test_day = test_day.strftime("%Y-%m-%d")
    new_group = {}    # 新开的素材方案
    close_group = {}   # 关闭的素材方案
    update_pic_data = {} # 素材变更内容

    if group_id == '':
        group_list = get_imagegroup_from_CMS(address)
    else:
        group_list = [group_id]

    today_test_result = {}
    for group in group_list:
        logging.info(group)
        url_release_data_prefixes = {
            "PBN_Lib": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?abtest_key={group}&limit=1&offset=0&status_list=ONLINE_LIBRARY&abtest_release_date_range=2015-08-01T00:00:00_{test_day}T00:00:00&paint_id=&abtest_show=true&category_id=&with_userscore=true&sort_by=release_date%5E-1",
            "PBN_Daily": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?abtest_key={group}&limit=50&offset=0&status_list=ONLINE_DAILY&abtest_daily_range=2015-08-01T00:00:00_{test_day}T00:00:00&paint_id=&abtest_show=true&sort_by=daily%5E-1",
            "ZC_Lib": f"https://zc-cms.learnings.ai/colorflow/v1/cms/abtest/{group}/detail?limit=1&offset=0&release_date=2018-07-10%5E{test_day}",
            "VC_Lib": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/abtest/{group}/detail?limit=1&offset=0&release_date=2018-07-10%5E{test_day}",
            "Vista_Lib": f"https://colorpad-cms.learnings.ai/colorpad/v1/cms/abtest/{group}/detail?limit=1&offset=0&release_date=2018-07-10%5E{test_day}",
            "BP_Lib": f"https://bpbncms.idailybread.com/bpbn/v1/cms/abtest/logic_item/{group}/list/trending?limit=20&offset=0&category_key=trending&size=&is_colored=false&is_gif=false&status=1&show_type=2&release_date_start=20150701&release_date_end={test_day}&id_or_filename=&with_scores=true"
        }
        url_day_prefixes = {
            "PBN_Lib": f"https://pbn-cms.learnings.ai/paint/v1/cms/paint?abtest_key={group}&limit=1&offset=0&status_list=ONLINE_LIBRARY&paint_id=&abtest_show=true&abtest_day_range=-100_100&category_id=&with_userscore=true&sort_by=release_date%5E-1",
            "ZC_Lib": f"https://zc-cms.learnings.ai/colorflow/v1/cms/abtest/{group}/detail?limit=1&offset=0&day=-100%5E100",
            "VC_Lib": f"https://vc-cms.learnings.ai/vitacolor/v1/cms/abtest/{group}/detail?limit=1&offset=0&day=-100%5E100",
            "Vista_Lib": f"https://colorpad-cms.learnings.ai/colorpad/v1/cms/abtest/{group}/detail?limit=1&offset=0&day=-100%5E100",
            "BP_Lib": f"https://bpbncms.idailybread.com/bpbn/v1/cms/abtest/logic_item/{group}/list/trending?limit=20&offset=0&category_key=trending&size=&is_colored=false&is_gif=false&status=1&show_type=1&id_or_filename=&with_scores=true"
        }
        url_release_data = url_release_data_prefixes.get(address)
        url_day = url_day_prefixes.get(address)
        total = 0
        for url in [url_release_data, url_day]:
            logging.info("url: %s", url)
            response = []
            if url is not None:
                try:
                    response = session.get(url, headers=CMS_headers)
                    response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
                except requests.exceptions.HTTPError as http_err:
                    logging.error(f"HTTP error occurred: {http_err}")
                except Exception as err:
                    logging.error(f"An error occurred: {err}")
                logging.info(response.json()["data"]["total"])
                total = response.json()["data"]["total"]+total
                logging.info("total: %s", total)
        today_test_result[group] = total
    logging.info("today_test_result: %s", today_test_result)

    test_result_filename = test_result_path + f"/{address}_test_result.json"
    if os.path.exists(test_result_filename):
        with open(test_result_filename, "r") as file:
            last_test_result = json.load(file)
            logging.info("last_test_result: %s", last_test_result)
            new_group = {key: today_test_result[key] for key in set(today_test_result.keys()) - set(last_test_result.keys())}
            close_group = {key: last_test_result[key] for key in set(last_test_result.keys()) - set(today_test_result.keys())}

            common_keys = set(today_test_result.keys()) & set(last_test_result.keys())
            update_pic_data = {key: today_test_result[key] - last_test_result[key] for key in common_keys}
            # update_pic_data = {key: value for key, value in update_pic_data.items() if value != 0}

            logging.info("new_group: %s", new_group)
            logging.info("close_group: %s", close_group)
            logging.info("update_pic_data: %s", update_pic_data)
    else:
        os.makedirs(os.path.dirname(test_result_filename), exist_ok=True)

    with open(test_result_filename, "w") as file:
        json.dump(today_test_result, file, indent=4)

    return new_group, close_group, update_pic_data