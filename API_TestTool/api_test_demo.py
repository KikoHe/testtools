# -*- coding:utf-8 -*-
import json,os,shutil
import requests
import pyminizip
import hashlib
import filetype

def downloadFile(fileId, url, savePath):
    # 将网页链接 url，文件夹路径 savePath 作为参数传入
    try:
        webPage = requests.get(url, timeout=5)
        #print(webPage.status_code)
        # 获取网页
        webContent = webPage.content
        # 网页内容
        file_type = filetype.guess(webContent).extension
        # 识别文件类型
        #print(file_type)
        file_path = savePath + fileId + '.' + file_type
        # 根据文件夹路径、文件名id、文件类型，组合文件保存路径
        f = open(file_path, 'wb')
        f.write(webContent)
        # 将网页内容写入保存路径中
        f.close()
    except requests.exceptions.RequestException:
        print(fileId + '超时')

def getjs():
    # 获取接口Json
    try:
        apiurl = "https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?offset=1&limit=2&ab_ignore_scheduled_paints=off"
        header = {"version": "1.19.1"}
        response = requests.get(url=apiurl, headers=header)
        js = json.loads(response.text)["data"]["content"]
        numbers = len(list(js))
        return js, numbers
    except requests.exceptions.RequestException:
        print(apiurl + '超时')

def checkJson(jsonname, keys):
    # 检查'jsonname'文件中是否有'keys'
    # 'jsonname'：文件名称
    # 'keys'：所有key数组,eg ['center', 'plans', 'area', 'subcolor']
    with open(jsonname) as f:
        temp = json.load(f)
    for jsonkey in keys:
        if jsonkey not in temp.keys():
            print(jsonkey+" key lose")
        elif (temp[jsonkey] == None):
            print(jsonkey+" value lose")

if __name__ == '__main__':
    shutil.rmtree('./zip')
    os.mkdir('./zip')
    # 初始化路径
    js, numbers = getjs()
    for i in range(numbers):
        id = js[i]["detail"][0]["id"]
        # 获取素材ID
        print(id + " Test " + str(i + 1))
        # 打印测试素材ID
        pictype = js[i]["detail"][0]["resource"]["color_type"]
        # 获取素材类型
        pwd_test = id+"VMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
        # pwd_test = "62ea3a681939d10001c4c59dVMyv=vJ?9ioBBxCu-naAlfyHXlW28F8#"
        password = hashlib.md5(pwd_test.encode('utf-8')).hexdigest()
        print(password)
        # 生成素材资源包密码

        zip = js[i]["detail"][0]["resource"]["zip"]
        zip_url = zip.split('cdn')
        zip_url_final = "https://cdn"+zip_url[1]
        # 获取并矫正资源包的CDN地址

        ospath = os.getcwd()
        path = ospath+"/zip/"+id
        filename = ospath+"/zip/"+id+'.zip'
        if not os.path.exists(path):
            os.makedirs(path)
        # 创建资源包的解压文件夹路径

        downloadFile(id, zip_url_final, './zip/')
        # 下载资源

        pyminizip.uncompress(filename, password, path, False)
        # 解压资源包到对应文件夹

        if os.path.exists('detail.json') is False:
            print(id+'json lose')
        else:
            checkJson('detail.json', ['center', 'plans', 'area', 'subcolor'])
        # 检查是否存在json文件，如果存在则检查keys是否存在

        # 检查资源内容
        if pictype == "COLORED":
            coloredpic = id+"_colored"
            if os.path.exists(coloredpic) is False:
                print(id + 'colored Fail')
        else:
            print("pass")
        # 检查资源内容

        os.chdir(ospath)
        # 切换回初始目录（这里坑了好久）

        continue