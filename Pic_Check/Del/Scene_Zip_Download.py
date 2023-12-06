import os
import requests
'''下载主题资源包'''

def download(pla):
    home = os.getcwd() + "/" + pla
    if os.path.exists(home) == False:
        os.mkdir(home)

    headers = {
        "platform": pla
    }
    url = "https://api-test.colorflow.app/colorflow/v1/collection/topic?offset=0&limit=10"
    response = requests.get(url, headers=headers)
    topics = response.json()["data"]["topics"]
    for i in range(len(topics)):
        # print("i"+str(i))
        sub_topics = topics[i]["sub_topics"]
        for i in range(len(sub_topics)):
            # print("ii" + str(i))
            main_color_file = sub_topics[i]["main_color_file"]
            title = sub_topics[i]["title"]
            print(main_color_file)
            r = requests.get(main_color_file)
            filename =home+"/"+str(title)+".zip"
            with open(filename, "wb") as code:
                code.write(r.content)

if __name__ == '__main__':

    platform = ['android','iOS']
    for pla in platform:
        download(pla)