import ast, os, glob, PyPDF2, fitz, json, inspect, shutil
import pytz, hashlib, zipfile, requests, pyzipper, subprocess, logging
from Common_Fun import *
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

current_directory = os.getcwd() #当前路路径
home = os.path.join(current_directory, "Pic")  ##下载的zip文件存放路径
if not os.path.exists(home):
    os.makedirs(home)
    print(f"文件夹 '{home}' 不存在，已创建")
test_result_path = os.path.join(current_directory, "Test_Result")  ##下载的zip文件存放路径
if not os.path.exists(test_result_path):
    os.makedirs(test_result_path)
    print(f"文件夹 '{test_result_path}' 不存在，已创建")

timezone = "Pacific/Apia"
timezone_cn = "Asia/Shanghai"

today = datetime.now(pytz.timezone(timezone))
formatted_date1 = today.strftime("%Y-%m-%d")
formatted_date2 = today.strftime("%Y%m%d")
formatted_date3 = today.strftime("%Y%m") ##当前月份

CMS_headers = {
    "Content-Type": "application/json",
    # "cookie": '''_ga=GA1.1.1929480831.1691656939; learnings-passport=_sLoatJ7zrLmUuJjAyErLhekSW3RsYzZ2lr6_ZzTsiHgDHFKnnZS0taYmRszx8Wp; isArtist=false; projectIds=[%225b84f58e689998000116d3fd%22%2C%225b892d3a9f9b4e00011d1cf3%22%2C%225e43d79dbfe4170001141436%22]; products=[%225bfb5a2b6ff9950001e9a969%22%2C%225c00dc5713ab060001c19ea0%22%2C%225b18ef419c560300013ddf28%22%2C%225b18f0079c560300013ddf29%22%2C%225e43d79dbfe4170001141436%22%2C%225b84f58e689998000116d3fd%22%2C%225b892d3a9f9b4e00011d1cf3%22%2C%22657953298aa0c540cc3fd85d%22%2C%22655d7180648210324dccb499%22%2C%2264b4c17796b49d036a8d6bb9%22%2C%2264b4c18196b49d036a8d6bba%22%2C%22645b2f85cd911b5ea8511fd6%22%2C%2260385d6148b726000118051b%22%2C%2260385d8448b726000118051c%22]; ajs_anonymous_id=42cd20ca-c89e-49ac-ad60-eb63ead5252c; uac_passport="2|1:0|10:1719804699|12:uac_passport|44:ZjhjY2Y1Y2ZhYmVlNDA4ZjgyN2I0NzdhYzQwNDYyOWY=|07278d3a26be700c22ec6c25569b9c2fcea8b391ea5e95806372d99497d945d3"; _ga_2Z4PFG28RG=GS1.1.1719818527.767.1.1719818529.58.0.0; learnings-user=Y9TMYRYvMgjahTWxYd_XFBI0KYZJaHUk1l1MhwgegnVgqXUGbYb7DNmGxEsuwcEcKbKBz9e5MNQayINWig9hTAD5eHvFRuEC7knIaO169ZErprdOkdMvq1R3gLWpyaLV-dUnBVgGFjIbeYsmdFSvoTOdMvSq9p5Gvr4myfyULiuUpZ5EAoD3kKYrdKfbt_-a588mMst8FAJJWkOi-4cJ7Pa52OtqzsQs31lDCAZmvdpzGYSG2w3AldQVQK1UpZm51dy3CFOAYsdi2BOJzrJgsUr6KLquPfSdQsaoZVmqYivEfdpxXHdKq2iNG8z4NoTUlZC89Ac7OHGsOnO6As258zSos0gonyTKoL123EUxmzDgItL285urGsoNe_0SFmM08bsfQvXAgpOBLONzNKIqZ90ofhOaFOu75cT1jy_WTPXpwcVfSmhJ3UWY0W9Qpn-k0q44183PEm5umFgVDLS516TaDVGTGeNHQG2gRbR6F6C7pe1C4psz8E4I8ira6aF4vCzFnbSEDbRehhIGs2zio_tPClr5GfRFN5LwZFYawLo-nXuf2tCD_uYe71Bg0zc-ez73BO56fFg4idxP2v99L3VEeYeugm7kDTxOof1-GhA'''
    "cookie": '''_ga=GA1.1.1084550949.1697188455; projectIds=[%225bfb5a2b6ff9950001e9a969%22%2C%225c00dc5713ab060001c19ea0%22]; _ga_2Z4PFG28RG=GS1.1.1722412372.47.1.1722412380.52.0.0; uac_passport="2|1:0|10:1722412380|12:uac_passport|44:N2I1NTYyMjc2ZGQzNDNkYWI0N2EzMmM5MjUxYjMzMzA=|98811f36842c0955d32c46399a26596e770c69838b9a5340e78fc24ac0f1ba86"; user="2|1:0|10:1722412380|4:user|672:eyJpZCI6IjVjODVjMmVkOWRlZjJjMDAwMTYzNmM0YiIsInVzZXJpZCI6IjE1NTIyNjk4Nzc3NDk2Mzg3Iiwib3BlbmlkIjoib3VfZjQ4MTQwZTVjYzNjYWNlYmJiMmU0MTAzNTQ2MTFjNDgiLCJuYW1lIjoiXHU0ZjU1XHU2ZDliIiwiYXZhdGFyIjoiaHR0cHM6XC9cL3MxLWltZmlsZS5mZWlzaHVjZG4uY29tXC9zdGF0aWMtcmVzb3VyY2VcL3YxXC92Ml85YWRjZjE5MC02YjVmLTQwMDEtODJjZS0xMjc4YzFhYjdlMmd+P2ltYWdlX3NpemU9bm9vcCZjdXRfdHlwZT0mcXVhbGl0eT0mZm9ybWF0PXBuZyZzdGlja2VyX2Zvcm1hdD0ud2VicCIsImVtYWlsIjoiaGV0YW9AZGFpbHlpbm5vdmF0aW9uLmJpeiIsImRlcGFydG1lbnQiOlsib2QtMmFmZWVmYjEyYjAzNzBjMmViOGIwMTk2Njg4ZjdiMDgiXSwiYWN0aXZlIjp0cnVlLCJqb2JudW1iZXIiOiIiLCJkaW5nZGluZ191c2VyaWQiOiIxNTUyMjY5ODc3NzQ5NjM4NyIsImZlaXNodV91c2VyaWQiOiI4MzExNDJlNSIsImhpcmVkIjoxOTcwfQ==|b760b557fa7b9737a3b94bbafa85a4d5c1c17353116619c340f033d26fe63b5a"; products=[%225bfb5a2b6ff9950001e9a969%22%2C%225c00dc5713ab060001c19ea0%22%2C%225b18ef419c560300013ddf28%22%2C%225b18f0079c560300013ddf29%22%2C%225e43d79dbfe4170001141436%22%2C%225b84f58e689998000116d3fd%22%2C%225b892d3a9f9b4e00011d1cf3%22%2C%22657953298aa0c540cc3fd85d%22%2C%22655d7180648210324dccb499%22%2C%2264b4c17796b49d036a8d6bb9%22%2C%2264b4c18196b49d036a8d6bba%22%2C%22645b2f85cd911b5ea8511fd6%22%2C%2260385d6148b726000118051b%22%2C%2260385d8448b726000118051c%22]'''
}

phone_headers = {
        "platform": "ios",
        "install_day": "100",
        "timezone": "Pacific/Apia",
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
        "device-type": "phone",
        "abtest_zip": "true"
    }

# 设置重试次数以及回退策略
retries = Retry(total=5,  # 总尝试次数
                backoff_factor=1,  # 回退等待时间的指数基数
                status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试
# 创建一个带有重试的会话对象
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# 创建一个日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建一个处理器将日志消息打印到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 创建一个处理器将warning和error级别的日志保存到文件
file_handler = logging.FileHandler(test_result_path+'/test.log')
file_handler.setLevel(logging.WARNING)  # 只保存warning和error级别的日志
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def example_function():
    logging.info('这是一个信息级别的日志消息')
    logging.warning('这是一个警告级别的日志消息')
    logging.error('这是一个错误级别的日志消息')