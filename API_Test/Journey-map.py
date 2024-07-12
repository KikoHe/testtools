import openpyxl,requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 设置重试次数以及回退策略
retries = Retry(total=5,  # 总尝试次数
                backoff_factor=1,  # 回退等待时间的指数基数
                status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

# 创建一个带有重试的会话对象
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))

def Get_All_PackID(LUID):
    headers = {
        "app": "paint.by.number.pixel.art.coloring.drawing.puzzle",
        "apiVersion": "2",
        "versionNum": "10702",
        "today": "20240423",
        "font_size": "1.0",
        "User-Agent": "android/31 paint.by.number.pixel.art.coloring.drawing.puzzle/4.0.0",
        "version": "4.1.0",
        "platform": "ios",
        "language": "en",
        "country": "US",
        "install_day": "0",
        "luid": LUID,
        "uuid": "f317e833a67a452c80c222aecc6fa052",
        "abtest_zip": "true",
        "cookie": '''user="2|1:0|10:1713339286|4:user|116:eyJ1c2VySWQiOiI2NjFmN2I5NjViMWFhNzRmZjEzYjYxNDkiLCJkZXZpY2VUb2tlbiI6IjE2YzBmYWU3NTlhYjQ0NDBhYWRmZWFhOWFiODZiODRmIn0=|6c1a17bf04ad39864455c0e95e6349b57ec30d0d2e7b38f11bfc589590041a65"''',
    }
    url = "http://paint-api-stage.dailyinnovation.biz/paint/v1/monitor/journey-map"
    response_data = {}
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return response_data["hit"]
def updateExcel(file_path):
    '''''
    :param file_path:传入一个excel文件，或者文件的绝对路径
    '''
    luid_list = []
    try:
        book = openpyxl.load_workbook(file_path)
    except Exception as e:
        # 如果路径不在或者excel不正确，返回报错信息
        print('路径不在或者excel不正确', e)
    else:
        sheet = book.active  # 取第一个sheet页
        y = 1500
        while y < 2000:
            luid = sheet.cell(row=y, column=1).value
            if luid is not None:
                luid_list.append(luid)
            y = y+1
    return luid_list

luid_list = updateExcel("/Users/ht/Downloads/results-20240423-194747.xlsx")
# luid_list = ["55d6e3f64bc311ed932f0242ac110006","fba8e81c9cec11ee9ea40242ac110013","a7a0e0faed0311eeb0080242ac110006","73dbe476b96011ee9ae00242ac11000d"]
for LUID in luid_list:
    a = Get_All_PackID(LUID)
    if str(a) == "True":
        print(str(LUID)+" 命中！")
    else:
        print(str(LUID)+" 未命中！")

