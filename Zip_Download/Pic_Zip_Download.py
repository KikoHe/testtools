import os
import requests
import zipfile
import tempfile
import hashlib
from PIL import Image
'''下载列表素材的zip包'''


# 'https://paint-api.dailyinnovation.biz/paint/v1/paintCategory/5ba31d31fe401a000102966e/paints?day=0&groupNumber=ios_c&limit=40&offset=0&pic_sort_new=a&require_cache=0&test_paint=1': {
# uuid = "6d4ff2bbc8424f67822500c27218e066";
# font_size = "17";
# version = "2.60.1";
# abtest_zip = "true";
# luid = "116937f6e09811eb8abb0242ac110005";
# versionNum = "2345";
# support-blend = "true";
# device-type = "phone";
# apiVersion = "2";
# app = "com.paint.bynumber";
# Accept-Language = "en;q=1";
# platform = "ios";
# User-Agent = "PaintByNumber/2.60.1 (iPhone; iOS 14.5; Scale/3.00)";
# language = "en";
# timezone = "Asia/Shanghai";
# country = "US";
# app_alias = "PBN";
# Cookie = "user="2|1:0|10:1627028981|4:user|116:eyJ1c2VySWQiOiI2MGZhN2RmNTYxMTM4ODY0MjY2ZjQyODIiLCJkZXZpY2VUb2tlbiI6ImJmODk2MDM1OTYwYjQzZDc5ODk3ODAxNjFmZjdjNTI0In0=|8fe50cfd6e6d13c978b0168461cefbdf83d03794c2d7b69a806ee88749a30ab8"";
# }
def getJson():
    # 获取素材列表数据
    headers = {
   }
    url = "https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?offset=0&limit=50&ab_ignore_scheduled_paints=off"
    response = requests.get(url, headers=headers)
    return response.json()


def getPaintDetail(pbnid):
    #获取素材详情接口内容
    url = "https://paint-api.dailyinnovation.biz/paint/v1/paint/%s" % (pbnid)
    res = requests.get(url)
    return res.json()


def getZipFronResource(responce):
    #获取素材各种属性
    if responce is None:
        print("responce is None")
        return None
    data = responce["data"]
    if data is None:
        print("data is None")
        return None
    paintList = data["paintList"]
    if paintList is None:
        print("paintList is None")
        return None
    result = []
    for paint in paintList:
        categoryArr = []
        for category in paint["category"]:
            categoryArr.append(category["id"])
        categoryStr = ",".join(categoryArr)
        temp = {
            "day": paint["day"],
            "id": paint["id"],
            "zip_file": paint["zip_file"],
            "line": paint["line"],
            "category": categoryStr
        }
        result.append(temp)
    return result


def convert(path):
    # print(name)
    webp_im = Image.open(path)
    rgb_im = webp_im.convert('RGB')
    new_name = path + '.png'
    rgb_im.save(new_name)

    # 转换格式后删除，如果不需要删除原来的webp文件，直接注释即可
    os.remove(path)


def downLoadZip(path, paintList):
    #下载并解压素材zip包
    if len(paintList) == 0:
        print("Zip_Download zip list none")
        return

    home = os.getcwd() + "/" + path
    if os.path.exists(home) == False:
        os.mkdir(home)
    for paint in paintList:
        zipResponse = requests.get(paint["zip_file"])
        content = zipResponse.content
        tempFile = tempfile.TemporaryFile()
        tempFile.write(content)

        paintId = paint["id"]
        password = paintId + "VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
        pwd = hashlib.md5(password.encode()).hexdigest()
        zf = zipfile.ZipFile(tempFile, mode='r')
        zf.setpassword(pwd.encode())
        for name in zf.namelist():
            f = zf.extract(name, './%s/%s' % (path, paintId))
        zf.close()

        detail = getPaintDetail(paintId)
        basePath = home + "/" + paintId + "/" + paintId
        centerPath = basePath + "_center.txt"
        with open(centerPath, 'w') as f:
            f.write(detail["data"]["center"])

        planPath = basePath + "_plan.txt"
        with open(planPath, 'w') as f:
            f.write(detail["data"]["plans"][0])

        planPath = basePath + "_info.txt"
        with open(planPath, 'w') as f:
            f.write(paint["category"])
        pdfPath = basePath + "_origin"
        pdfPath2 = pdfPath + ".pdf"
        if os.path.exists(pdfPath):
            os.system("mv %s %s" % (pdfPath, pdfPath2))

        coloredPath = basePath + "_colored"
        if os.path.exists(coloredPath):
            convert(coloredPath)

        regionPath = basePath + "_region"
        if os.path.exists(regionPath):
            convert(regionPath)

if __name__ == '__main__':
    day0paints = getJson(False)
    day0zips = getZipFronResource(day0paints)

    day0zipsNew = list(filter(lambda x: x["day"] == 0, day0zips))
    downLoadZip("day0", day0zipsNew)

    dayUpdatepaints = getJson(True)
    dayUpdateZips = getZipFronResource(dayUpdatepaints)
    dayUpdateZipsNew = list(filter(lambda x: x["day"] == 1, dayUpdateZips))
    downLoadZip("day_update", dayUpdateZipsNew)

