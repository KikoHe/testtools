import os,glob
from PIL import Image
import requests,json
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 设置重试次数以及回退策略
retries = Retry(total=5,  # 总尝试次数
                backoff_factor=1,  # 回退等待时间的指数基数
                status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))

def upload_pic_get_url(image_path):
    upload_api = f"https://cw-lens.dailyinnovation.biz/upload"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    data = {'path': 'paintByNumber'}
    try:
        with open(image_path, 'rb') as file:
            files = {'file': file}
            response = session.post(upload_api, headers=headers, files=files, data=data)
            response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常

        response_data = response.json()["data"]
        print(response_data["url"])
        return response_data["url"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def send_feishu_image(image_path,image_name):
    api = "https://work.learnings.ai/notify-gateway/v1/msg"
    url = upload_pic_get_url(image_path)
    data = {
        "notifyMethod": [
            "feishu"
        ],
        "msgType": "markdown",
        "msgTitle": f"{image_name}",
        "msgContent": f"**测试图片**\n![pic]({url})",
        "notifyConfig": {
            "feishu": {
                "notifyType": "chat",
                "chatId": "65ba3d36a67ee10ed604fe75",
                "render": {
                    "titleColor": "carmine"
                }
            }
        },
        "sendMode": "async"
    }
    response = requests.post(api, json=data)
    print(response.text)
def send_testimage_to_feishu():
    # 设定图片文件夹的名称，这个文件夹位于当前工作目录下
    image_folder_name = 'screenshots'
    # 当前工作目录的路径
    current_directory = os.getcwd()
    # 图片文件夹的完整路径
    image_folder_path = os.path.join(current_directory, image_folder_name)
    # 支持的图片格式列表
    image_formats = ['*.png', '*.jpeg', '*.jpg', '*.gif', '*.bmp']
    # 列出所有的图片文件
    image_files = []
    for image_format in image_formats:
        # 使用glob.glob匹配所有格式的文件
        image_files.extend(glob.glob(os.path.join(image_folder_path, image_format)))
    # 打印找到的所有图片文件路径
    for image_file in image_files:
        print(image_file)
        image_name = os.path.basename(image_file)
        send_feishu_image(image_file, image_name)

send_testimage_to_feishu()