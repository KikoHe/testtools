from Test_case import *
from Public_env import *

# 发送测试报告:PBN故事书、Vista素材包更新
def report_test_update_pic_from_api():
    output = test_update_pic_from_api(address_input=['PBN_Story', 'Vista_Pack'])
    logging.info("output: %s", output)
    summary = ""
    for data in output:
        project = list(data.keys())
        value = data[project[0]]

        update_pics = value[0]
        update_ids_output = f" 更新素材：{update_pics}张"

        error_ids = value[1]
        if error_ids == []:
            error_ids_output = "没有发现异常素材"
        else:
            error_ids_output = f"发现异常素材ID：{error_ids}"

        summary = summary + f"{project[0]}： \n1、{update_ids_output}；\n2、{error_ids_output}；\n\n"
    logging.info(f"SUMMARY: {summary}")
    return summary

# 发送测试报告：默认Group的Lib和Daily模块的素材张数，及资源是否正确
def report_test_releaseday_pic_from_cms(release_day):
    output = test_releaseday_pic_from_cms('', release_day)
    logging.info("output: %s", output)
    summary = ""
    for data in output:
        project = list(data.keys())
        value = data[project[0]]

        update_pics = value[0]
        update_ids_output = f" 更新素材：{update_pics}张"

        error_ids = value[1]
        if error_ids == []:
            error_ids_output = "没有发现异常素材"
        else:
            error_ids_output = f"发现异常素材ID：{error_ids}"

        summary = summary + f"{project[0]}： \n{update_ids_output}；{error_ids_output}\n"
    logging.info(f"SUMMARY: {summary}")
    return summary

# 发送检测报告：所有素材实验方案的配置
def report_check_CMS_pic_config(release_day):
    new_group_output, close_group_output, update_group_output, summary = '', '', '', ''
    address_list = ["PBN_Lib", "PBN_Daily", "ZC_Lib", "VC_Lib", "Vista_Lib"]
    for address in address_list:
        today_update_number = len(get_release_day_picid_from_cms(address, release_day))
        new_group, close_group, update_group = check_CMS_pic_config("", address, release_day)
        update_group = {key: value for key, value in update_group.items() if value != today_update_number} # 找出素材变量不等于每日更新的方案
        if new_group != {}:
            new_group_output = f"有上新的素材方案及对应素材数量：{new_group}，请确认是否正确"
        else:
            new_group_output = "没有上新素材方案"
        if close_group != {}:
            close_group_output = f"关闭的素材方案及素材数量：{close_group}，请确认是否正确"
        else:
            close_group_output = "没有关闭素材方案"
        if update_group != {}:
            update_group_output = f"素材变化数量如下：{update_group}，请确认是否正确【这里会排除：素材数量变化 = 每日更新素材 的素材方案】"
        else:
            update_group_output = f"所有素材方案正常更新素材！"


        summary = summary + f"{address}：\n1、{new_group_output}；\n2、{close_group_output}；\n3、 {update_group_output}\n\n"
    return summary

# 飞书消息发送函数
def send_feishu_summary_message(summary, webhook_url, title):
    # 构建JSON格式的消息体
    json_payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"{title}报告总结"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": summary
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "note",
                    "elements": [
                        {
                            "tag": "plain_text",
                            "content": "请检查上述项目并采取必要措施。"
                        }
                    ]
                }
            ],
            "mentioned_list": ["all"]
        }
    }
    # 使用requests库发送POST请求
    response = requests.post(webhook_url, json=json_payload)
    print(response.text)

if __name__ == "__main__":
    # webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/c7dbaf7d-3c94-46a4-872d-d819a650b1dc"
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/2ba28d6d-6765-4e54-85ac-bbfef081bc83"

    if today.weekday() <= 4:  # 周内仅执行当天的检查

        title_1 = f"{formatted_date1}素材实验方案配置检查"
        summary_1 = report_check_CMS_pic_config(today)
        send_feishu_summary_message(summary_1, webhook_url, title_1)

        title_2 = f"{formatted_date1}更新素材内容检查"
        summary_2 = report_test_releaseday_pic_from_cms(today)
        send_feishu_summary_message(summary_2, webhook_url, title_2)

    elif today.weekday() == 5:  # 周末执行两天的检查
        for i in range(2):
            next_day = today + timedelta(days=i)

            title_1 = f"{formatted_date1}素材实验方案配置检查"
            summary_1 = report_check_CMS_pic_config(next_day)
            send_feishu_summary_message(summary_1, webhook_url, title_1)

            title_2 = f'''{next_day.strftime("%Y-%m-%d")}素材方案检测'''
            summary_2 = report_test_releaseday_pic_from_cms(next_day)
            send_feishu_summary_message(summary_2, webhook_url, title_2)

    title_3 = f"{formatted_date1}PBN故事书、Vista素材包更新内容检查"
    summary_3 = report_test_update_pic_from_api()
    send_feishu_summary_message(summary_3, webhook_url, title_3)


    # title_debug = f"{formatted_date1}检测详细日志"
    # with open(f"{test_result_path}/test.log", 'r') as log:
    #     summary_debug = log.read()
    # send_feishu_summary_message(summary_debug, webhook_url, title_debug)