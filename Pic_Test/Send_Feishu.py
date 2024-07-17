import logging

from Test_case import *

output = test_update_pic_single_by_single()
# output = [{'PBN_Lib': [15, ['6690e0754a98b8c414e02db5'], []]}, {'PBN_Daily': [1, ['6690e0754a98b8c414e02db5'], []]}, {'PBN_Story': [0, ['6690e0754a98b8c414e02db5'], []]}, {'ZC_Lib': [8, ['6690e0754a98b8c414e02db5'], []]}, {'ZC_Daily': [1, ['6690e0754a98b8c414e02db5'], []]}, {'VC_Lib': [8, ['6690e0754a98b8c414e02db5'], []]}, {'VC_Daily': [1, ['6690e0754a98b8c414e02db5'], []]}, {'Vista_Lib': [6, ['6690e0754a98b8c414e02db5'], []]}, {'Vista_Daily': [1, ['6690e0754a98b8c414e02db5'], []]}, {'Vista_Pack': [0, ['6690e0754a98b8c414e02db5'], []]}, {'BP_Lib': [6, ['6690e0754a98b8c414e02db5'], []]}, {'BP_Daily': [1, ['6690e0754a98b8c414e02db5'], []]}]
logging.info("output: %s", output)

update_ids_output = ""
error_ids_output = ""
error_groups_output = ""
summary = ""

for data in output:
    print("data", data)
    project = list(data.keys())
    print("project:", project)
    value = data[project[0]]
    print("value", value)

    update_pics = value[0]
    update_ids_output = f" 更新素材：{update_pics}张"

    error_ids = value[1]
    if error_ids == []:
        error_ids_output = "没有发现异常素材"
    else:
        error_ids_output = f"发现异常素材ID：{error_ids}"

    error_groups = value[2]
    if error_groups == []:
        error_groups_output = "所有方案更新素材数量一致"
    else:
        error_groups_output = f"此方案更新素材数量和其他方案不一致：{error_groups}"
    summary = f"{project} - {update_ids_output}； {error_ids_output}； {error_groups_output}\n\n" + summary

logging.info(f"SUMMARY: {summary}")

# 飞书消息发送函数
def send_feishu_summary_message(summary, date):
    webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/2ba28d6d-6765-4e54-85ac-bbfef081bc83"
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
                    "content": f"{date}素材检测报告总结"
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

# 发送汇总消息
send_feishu_summary_message(summary, formatted_date1)