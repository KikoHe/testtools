import json, pytz, hashlib, zipfile, os, requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 设置重试次数以及回退策略
retries = Retry(total=5,  # 总尝试次数
                backoff_factor=1,  # 回退等待时间的指数基数
                status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

# 创建一个带有重试的会话对象
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))
# 已购买的包ID
# 全部包ID
# 调用API，通过输入的"已购买ID"、"概率类型"，请求返回的素材ID
def Get_Bonus_PackID():
    Purchased_Packid = []
    Purchase_Weights = 1 #权重
    Need_Bonus_Pack_Number = 2
    Bonus_PackID = []
    ...
    return Bonus_PackID

def Get_Pack_Level(PackID):
    headers = {
        "platform": "android",
        "install_day": "100",
        "country": "US",
        "version": "4.4.10",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
        "user-agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.4.10"
    }
    url = ""
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
        return response_data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    Price = response_data[""]
    if Price > "249":
        Level = 3
    return Level

