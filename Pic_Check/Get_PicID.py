import json
import requests

def Get_PicIDList(Project,limit):
    # 获取图库页素材列表地址
    url_prefixes = {
        "ZC": "https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?limit=" + str(limit),
        "PBN": "https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5ba31d31fe401a000102966e/paints?day=100&limit=" + str(limit),
        "VC": "https://vitacolor-api.vitastudio.ai/vitacolor/v1/paintcategory/all/paints?limit=" + str(limit)
    }
    url = url_prefixes.get(Project, "https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5ba31d31fe401a000102966e/paints")
    headers= {"platform": "ios", "install_day":"100", "timezone":"Asia/Shanghai"}
    response = requests.get(url, headers=headers)
    response_data = response.json()["data"]
    Pic_ids = []
    if Project == "PBN":
        paintList = response_data["paintList"]
        for item in paintList:
            Pic_ids.append(item["id"])
    elif Project in ["ZC", "VC"]:
        content = response_data["content"]
        for detail_content in content:
            Pic_ids.append(detail_content["detail"][0]["id"])
    return Pic_ids

def get_today_pic():
    headers_PBN = {
        "platform": "ios",
        "today": "20231205"
    }
    headers_ZCVC = {
        "platform": "ios",
        "data": "20231205"
    }
# if __name__ == '__main__':
#     print(len(Get_PicIDList("PBN")))
