# 构建大量着色素材：活动列表素材，转换为同步数据json，增量发送到账户中
import requests,pytz,json,os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime

timezone = "Pacific/Apia"
timezone_cn = "Asia/Shanghai"
today = datetime.now(pytz.timezone(timezone))
formatted_date1 = today.strftime("%Y-%m-%d")
formatted_date2 = today.strftime("%Y%m%d")
# 设置重试次数以及回退策略
retries = Retry(total=5,  # 总尝试次数
                backoff_factor=1,  # 回退等待时间的指数基数
                status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

# 创建一个带有重试的会话对象
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))
# 获取PBN分类素材列表的所有素材ID
def Get_pic_id_from_url(url):
    headers = {
        "platform": "android",
        "support-blend": "true",
        # "install_day": "100",
        "timezone": timezone,
        "today": "20240204",
        "country": "CN",
        "version": "4.6.6",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
        "luid": "fff633ea0aa311ebb5450242ac110006",
        "uuid": "9d1105f6de6f487eb9e8d21d07c2eda0",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.6.6"
    }
    try:
        id_list = []
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]["paintList"]
        for data in response_data:
            id = data["id"]
            id_list.append(id)
        return id_list
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 获取账户中的所有素材ID：未跑通
def Get_pic_id_from_syncall():
    url = "https://paint-api.dailyinnovation.biz/paint/v1/user/sync"
    headers = {
        "app": "paint.by.number.pixel.art.coloring.drawing.puzzle",
        "support-blend": "true",
        "apiversion": "2",
        "versionnum": "10970",
        "timezone": "Asia/Shanghai",
        "today": "20240202",
        "font_size": "1.0",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.6.6",
        "version": "4.6.6",
        "platform": "android",
        "language": "zh-Hans",
        "country": "CN",
        "luid": "fff633ea0aa311ebb5450242ac110006",
        "uuid": "9d1105f6de6f487eb9e8d21d07c2eda0",
        "abtest_zip": "true",
        "Content-Type": "application/json",
        "content-length": "74",
        "accept-encoding": "gzip",
        "cookie": '''user="2|1:0|10:1706866960|4:user|116:eyJ1c2VySWQiOiI2NWJjNTdmOTI2N2U1ZjYyYmMzNDQwNWYiLCJkZXZpY2VUb2tlbiI6IjIzNTU4YzJkYTRjYzRlNzY5NDY5MjgwZmYwYTk0ZGQ2In0=|d8093f846978848298a554f28be8b4bb832849cfad1375813375493cb1d44792"'''
    }
    try:
        id_list = []
        response = session.get(url, headers=headers, timeout=60)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]["work"]
        print("start...")
        for data in response_data:
            id = data["paint"]["id"]
            print(id)
            id_list.append(id)
        print(len(id_list))
        return id_list
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 获取XXX分类的素材ID
def get_pic_id_more():
    url = "https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5c90960434d5a60001f6f7d1/paints?limit=30000&offset=0&day=0&contain_colored=yes&show_d0_release=true&test_paint=false&groupNumber=c&pic_sort_new=a"
    old_ids = Get_pic_id_from_url(url)
    print("所有图片数:" + str(len(old_ids)))
    # 检查文件是否存在，如果不存在则创建新文件并写入默认内容
    if not os.path.exists('sync_all.txt'):
        with open('sync_all.txt', 'w') as file:
            default_data = {"data": {"work_list": []}}
            json.dump(default_data, file)
    # 读取JSON数据文件
    with open('sync_all.txt', 'r') as file:
        content = file.read()
        json_data = json.loads(content)
    synv_id_list = []
    for data in json_data["data"]["work_list"]:
        id = data["paint"]["id"]
        synv_id_list.append(id)
    result = [x for x in old_ids if x not in synv_id_list]
    return result

# 推送单个数据到账户中
def post_data():
    url = "https://paint-api.dailyinnovation.biz/paint/v1/sync/paint"
    headers = {
        "app":"paint.by.number.pixel.art.coloring.drawing.puzzle",
        "support-blend":"true",
        "apiversion": "2",
        "versionnum": "10970",
        "timezone":"Asia/Shanghai",
        "today":"20240202",
        "font_size":"1.0",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.6.6",
        "version": "4.6.6",
        "platform": "android",
        "language": "zh-Hans",
        "country": "CN",
        "luid": "fff633ea0aa311ebb5450242ac110006",
        "uuid": "9d1105f6de6f487eb9e8d21d07c2eda0",
        "abtest_zip":"true",
        "Content-Type": "application/json",
        "content-length":"74",
        "accept-encoding":"gzip",
        "cookie": '''user="2|1:0|10:1718271442|4:user|116:eyJ1c2VySWQiOiI2NjZhYmRkMjZjOTVhMmQ1MzA0NzFkYmUiLCJkZXZpY2VUb2tlbiI6IjgyYzNjMzIxMTlkZTQwODhiZmMzNjE2ZGMzNGY4NDI1In0=|f0272423786eb8d0642ca2d300a833e1b6fccaa0df217f49d180dbf072f278fd"'''
    }
    data_pic = {"lastModified": 1706842086027, "paintId": "5d289a8ba5b37f00014592e8", "state": 2}
    try:
        response = requests.post(url, json=data_pic, headers=headers,  timeout=60)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}, {http_err.response.content}")
    except Exception as err:
        print(f"An error occurred: {err}")

# 循环推送素材到账户中
def post_work_list():
    url = "https://paint-api.dailyinnovation.biz/paint/v1/sync/paint"
    headers = {
        "app":"paint.by.number.pixel.art.coloring.drawing.puzzle",
        "support-blend":"true",
        "apiversion": "2",
        "versionnum": "10970",
        "timezone":"Asia/Shanghai",
        "today":"20240202",
        "font_size":"1.0",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.6.6",
        "version": "4.6.6",
        "platform": "android",
        "language": "zh-Hans",
        "country": "CN",
        "luid": "fff633ea0aa311ebb5450242ac110006",
        "uuid": "9d1105f6de6f487eb9e8d21d07c2eda0",
        "abtest_zip": "true",
        "Content-Type": "application/json",
        "content-length": "74",
        "accept-encoding": "gzip",
        "cookie": '''user="2|1:0|10:1718280719|4:user|116:eyJ1c2VySWQiOiI2NjYyZGE4NTIwNmNjOGVjM2ZjYWJhMmIiLCJkZXZpY2VUb2tlbiI6ImQzMzAzMDdmM2Y0NzQ5MWM5MmM1OGVhYTIwYTIzYTNiIn0=|c327b7208f856389b423fc99b6cb0581dfdaad7518961134eec8bdee232e0cb9"'''
    }
    key = 1
    paint_ids = get_pic_id_more()
    for paint_id in paint_ids:
        work_item = {
            "lastModified": 1718280587,
            "paintId": paint_id,
            "state": 2
        }
        try:
            response = session.post(url, json=work_item, headers=headers, timeout=60)
            response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
            print(key)
            print(work_item)
            key = key + 1
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}, {http_err.response.content}")
        except Exception as err:
            print(f"An error occurred: {err}")
post_work_list()

# 成就
def get_infofof():
    file = open('excel/badge.json', 'r')
    content = file.read()
    json_data = json.loads(content)
    file.close()
    claim_period_str = json_data["claim_period_str"]
    print(len(claim_period_str))
# get_infofof()