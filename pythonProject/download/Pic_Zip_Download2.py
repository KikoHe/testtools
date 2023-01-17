import requests,shutil
import hashlib,zipfile,os

# 下载指定url的素材zip包
def getJson():

    #创建下载目录
    home = os.getcwd() + "/" + "download"
    if os.path.exists(home) == False:
        os.mkdir(home)
    shutil.rmtree(home)
    #抓包
    headers = {
        "platform": "ios"
    }
    url = "https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?offset=0&limit=2000&ab_ignore_scheduled_paints=off"
    response = requests.get(url, headers=headers)
    content = response.json()["data"]["content"]
    for i in range(len(content)):
        id = content[i]["detail"][0]["id"]
        zip = content[i]["detail"][0]["resource"]["zip"]
        region_json_zip = content[i]["detail"][0]["resource"]["region_json_zip"]
        color_type = content[i]["detail"][0]["resource"]["color_type"]

        #计算密码
        passwordid = id + "VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
        pwd = hashlib.md5(passwordid.encode()).hexdigest()

        # #下载zip包
        # if color_type == "NORMAL":
        #     r = requests.get(zip)
        #     filename = str(id)+".zip"
        #     with open(filename, "wb") as code:
        #         code.write(r.content)
        #
        #
        #     #解压zip包
        #     zf = zipfile.ZipFile(filename, mode='r')
        #     zf.setpassword(pwd.encode())
        #     for name in zf.namelist():
        #         f = zf.extract(name, './%s/%s' % ("download", id))
        #     zf.close()
        # os.remove(filename)

        #下载region_json_zip包
        if region_json_zip != None:
            r1 = requests.get(region_json_zip)
            filenamenew = str(id) + ".zip"
            with open(filenamenew, "wb") as code:
                code.write(r1.content)
            # 解压zip包
            zf1 = zipfile.ZipFile(filenamenew, mode='r')
            zf1.setpassword(pwd.encode())
            for name in zf1.namelist():
                f = zf1.extract(name, './%s/%s' % ("download", id))
            zf1.close()
            os.remove(filenamenew)

if __name__ == '__main__':
    getJson()