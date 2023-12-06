import json
import requests,shutil
import hashlib,zipfile,os

# 下载指定url的素材zip包
def getJson():
    #创建下载目录
    home = os.getcwd() + "/" + "Pic_Check"
    if os.path.exists(home) == False:
        os.mkdir(home)
    shutil.rmtree(home)
    #抓包
    headers = {
        "platform": "ios"
    }
    url = "https://api.colorflow.app/colorflow/v1/paintcategory/all/paints?offset=0&limit=1&ab_ignore_scheduled_paints=off"
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

        #下载zip包
        if color_type == "NORMAL":
            r = requests.get(zip)
            filename = str(id)+".zip"
            with open(filename, "wb") as code:
                code.write(r.content)
            #解压zip包
            zf = zipfile.ZipFile(filename, mode='r')
            zf.setpassword(pwd.encode())
            for name in zf.namelist():
                f = zf.extract(name, './%s/%s' % ("Pic_Check", id))
            zf.close()

        filename = home + "/" + id + "/" + "detail.json"
        with open(filename, "r") as file:
            data = json.load(file)
            center = data["center"]
            center_number = center.split('|')  # 色块数
            center_number_code_list = []
            for i in range(len(center_number)):
                center_number_code = center_number[i-1].split(',')[0]
                center_number_code_int = int(center_number_code)
                center_number_code_list.insert(-1, center_number_code_int)
            print(sorted(center_number_code_list))
            plan = data["plans"]
            plan_number = plan[0].split('|')  # 色号数
            plan_number_code_list = []
            for i in range(len(plan_number)):
                plan_number_code = plan_number[i].split('#')[0].split(',')
                for num in range(len(plan_number_code)):
                    plan_number_code_single = plan_number_code[num-1]
                    plan_number_code_int = int(plan_number_code_single)
                    plan_number_code_list.insert(-1, plan_number_code_int)
            print(sorted(plan_number_code_list))
        if sorted(center_number_code_list) != sorted(plan_number_code_list):
          print(id + f" 的Center、Plan 色块不完全一致")
          difference = set(plan_number_code_list) - set(center_number_code_list)
          if difference:
              raise ValueError(f"Plan中含有Center中没有的元素: {difference}")
        os.remove(filename)
        #下载region_json_zip包
        # if region_json_zip != None:
        #     r1 = requests.get(region_json_zip)
        #     filenamenew = str(id) + ".zip"
        #     with open(filenamenew, "wb") as code:
        #         code.write(r1.content)
        #     # 解压zip包
        #     zf1 = zipfile.ZipFile(filenamenew, mode='r')
        #     zf1.setpassword(pwd.encode())
        #     for name in zf1.namelist():
        #         f = zf1.extract(name, './%s/%s' % ("Pic_Check", id))
        #     zf1.close()
        #     os.remove(filenamenew)
if __name__ == '__main__':
    getJson()
