from Test_case import *

# 发送每日更新素材的测试报告
def report_test_update_pic_single_by_single():
    output = test_update_pic_single_by_single()
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

        error_groups = value[2]
        if error_groups == []:
            error_groups_output = "所有方案更新素材数量一致"
        else:
            error_groups_output = f"此方案更新素材数量和其他方案不一致：{error_groups}"
        summary = f"{project} - {update_ids_output}； {error_ids_output}； {error_groups_output}\n\n" + summary
    logging.info(f"SUMMARY: {summary}")
    return summary

# 发送素材方案内容检测报告
def report_check_CMS_pic_config():
    new_group_output,close_group_output,update_group_output,summary = '', '', '', ''
    address_list = ["PBN_Lib", "ZC_Lib", "VC_Lib", "Vista_Lib"]
    # address_list = ["ZC_Lib"]
    for address in address_list:
        new_group, close_group, update_group = check_CMS_pic_config("", address)
        if new_group != {}:
            new_group_output = f"最近上新素材方案及素材数量：{new_group}，请确认是否正确"
        else:
            new_group_output = "最近没有上新素材方案"
        if close_group != {}:
            close_group_output = f"最近关闭素材方案及素材数量：{close_group}，请确认是否正确"
        else:
            close_group_output = "最近没有关闭素材方案"
        if update_group != {}:
            update_group_output = f"最近素材方案的素材变化：{update_group}，请确认是否正确"

        summary = f"{address} - {new_group_output}； {close_group_output}； {update_group_output}\n\n" + summary
    return summary

# 飞书消息发送函数
def send_feishu_summary_message(summary, date, webhook_url, title):
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
                    "content": f"{date}{title}报告总结"
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

    # title_1 = "素材方案检测"
    # summary_1 = report_test_update_pic_single_by_single()
    # send_feishu_summary_message(summary_1, formatted_date1, webhook_url, title_1)

    title_2 = "当日更新素材资源检测"
    summary_2 = report_check_CMS_pic_config()
    send_feishu_summary_message(summary_2, formatted_date1, webhook_url, title_2)