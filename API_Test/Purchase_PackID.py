import json, pytz, hashlib, zipfile, os, requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from collections import Counter

# 设置重试次数以及回退策略
retries = Retry(total=5,  # 总尝试次数
                backoff_factor=1,  # 回退等待时间的指数基数
                status_forcelist=[500, 502, 503, 504])  # 指定哪些状态码需要进行重试

# 创建一个带有重试的会话对象
session = requests.Session()
session.mount('https://', HTTPAdapter(max_retries=retries))
# 已购买的包ID
# 全部包ID
# 调用API，通过输入的"已购买ID"、"概率类型"，请求返回的素材I

def Get_All_PackID():
    headers = {
        "platform": "ios",
        "install_day": "100",
        "country": "US",
        "language": "zh-Hans",
        "apiversion": "2",
        "versionnum": "10899",
    }
    url = "https://colorpad-api-stage.vitastudio.ai/colorpad/v1/paint/pack?limit=60&offset=0"
    Pack_data_list = []
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    for data in response_data["content"]:
        Packid = data["id"]
        Price = data["price"]
        Pack_data = {Packid:Price}
        Pack_data_list.append(Pack_data)
    total = response_data["total"]
    # print(total)
    if total == len(Pack_data_list):
        ...
    else:
        print("包数量不对！！！")
    return Pack_data_list
# print(Get_All_PackID())

def Get_All_Pack_Level(level):
    All = Get_All_PackID()
    if level == 3:
        selected_keys = [list(d.keys())[0] for d in All if list(d.values())[0] > 300]
    elif level == 2:
        selected_keys = [list(d.keys())[0] for d in All if 300 >= list(d.values())[0] > 150]
    elif level == 1:
        selected_keys = [list(d.keys())[0] for d in All if 150 >= list(d.values())[0]]
    print("Level"+str(level)+"的所有包ID： " + str(selected_keys))
    return selected_keys
# Get_All_Pack_Level(3)

def Get_Bonus_PackID(Purchased_PackID,count,high_pack_count):
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
    url = "https://colorpad-api-stage.vitastudio.ai/colorpad/v1/paint/pack/luckydraw"
    body = {
        "purchased_pack_ids": Purchased_PackID,
        "count": count,
        "bonus_pack_count": high_pack_count
    }
    # print(body)
    Pack_data_list = []
    response_data = {}
    try:
        response = session.put(url, headers=headers, json=body)
        response.raise_for_status()  # 如果请求返回的状态码不是200，则抛出异常
        response_data = response.json()["data"]["content"]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    for data in response_data:
        Packid = data["id"]
        Price = data["price"]
        Pack_data = {Packid: Price}
        Pack_data_list.append(Pack_data)
    return Pack_data_list

# print(Get_Bonus_PackID([],"2","false"))
# Get_Bonus_PackID([],"2","false")

# 测试:权重
# 测试:奖励包ID 不能是 已购买包ID
def Test_1(input, times, count, high_pack_count=0):
    if input == 1 or input == 2 or input == 3:
        Purchased_PackID = Get_All_Pack_Level(input) #1、2、3代表各自等级的全部包
        if input == 1:
            print("level 1的包都被购买了")
        elif input == 2:
            print("level 2的包都被购买了")
        elif input == 3:
            print("level 3的包都被购买了")
    else:
        Purchased_PackID = input #具体ID
    print("已购素材包ID： " + str(Purchased_PackID))
    if high_pack_count == 0:
        print("固定权重")
    else:
        print("特殊权重")
    Level_list = [] #奖励包的等级
    PackID_total_list = []
    i = 0
    while True:
        if i >= times:
            print("重复购买了："+str(times)+"次")
            break
        Bonus_Pack = Get_Bonus_PackID(Purchased_PackID, count, high_pack_count) # 获取奖励包数据

        Bonus_Pack_ID_list = [list(d.keys())[0] for d in Bonus_Pack]
        Return_PackID = list(Bonus_Pack_ID_list)
        print("Return_PackID: " + str(Return_PackID))

        PackID_total_list.append(Return_PackID) #收集所有购买的包ID
        Bonus_Pack_price_list = [list(d.values())[0] for d in Bonus_Pack] # 获取奖励包价格
        for price in Bonus_Pack_price_list:  # 将包的等级存入Level_list
            if price > 300:
                Level_list.append(3)
            elif price > 150:
                Level_list.append(2)
            else:
                Level_list.append(1)
        if input != 3 and high_pack_count != 0:
            # print("单次购买的奖励包ID："+str(PackID_total_list))
            # print("单次购买的奖励包等级："+str(Level_list))
            if 3 not in Level_list:
                print("特殊权重，没有奖励level3的素材")
            else:
                print("特殊权重，奖励了level3的素材")
                number = 0
                while True:
                    Level_list.remove(3)
                    number = number + 1
                    if number >= high_pack_count:
                        break

        # 将两个列表转换为集合
        Purchased_PackID_set = set(Purchased_PackID)
        Return_PackID_set = set(Return_PackID)
        # 检查两个集合是否有交集（是否有相同的元素）
        Failed_PackID = Purchased_PackID_set.intersection(Return_PackID_set)
        if Failed_PackID:
            print("错误：返回了已购买的包"+str(Failed_PackID))
        else:
            print("正常：没有返回已购买的包")
        i = i+1
    print("多次购买后的奖励素材包ID： " + str(PackID_total_list))
    print("多次购买后的奖励素材包等级： " + str(Level_list))

    level_counts = Counter(Level_list)# 计算总的元素个数
    total_count = len(Level_list)# 计算每个元素的比例
    level_weights = {level: count / total_count for level, count in level_counts.items()}
    for level, weight in level_weights.items():  # 打印每个元素的比例
        print(f"等级 {level} 的比例为: {weight:.2f}")

# 已购包ID、购买次数、单次购买个数、高价值包个数
Test_1("", 1, 4, 3)