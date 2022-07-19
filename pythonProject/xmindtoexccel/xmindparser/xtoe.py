# -*- coding: utf-8 -*-

import os
import json
import data.excelTool
from openpyxl import Workbook
from xmindparser import xmind_to_dict

#记录列数，全局变量，还原方便
columnIndex = 1
#记录行数
rowIndex = 1
#每个完整用例子主题的个数
caseCount = 0
#同层级主题个数
level_equal = 0


def get_xmind_zen_dict(ws, case_topics,main_topic):
    """
    :param case_topics: 用例集
    :return:

    遍历过程中需要有以下标记
    1、层级标记：主标题 - 分支标题 - 同级标题 - 子标题
    2、用例条数：对应Excel的行数

    """
    # 首层
    feature_topic_count = len(case_topics)
    global rowIndex
    global columnIndex
    global caseCount
    global level_equal

    # 遍历用例集，直到无topics表示用例遍历完成
    for index in range(0, feature_topic_count):
        # 当前层级主题的标题
        topic_title = case_topics[index]['title']
        print(topic_title)

        #将已经提取出来的外层主题进行对比，设置为最外层的用例名
        if topic_title in main_topic:
            columnIndex = 1

        # 首先，将主功能占位
        data.excelTool.setCellValue(ws=ws, columnIndex=columnIndex, rowIndex=rowIndex,
                                    value=topic_title)
        columnIndex += 1

        if 'topics' in case_topics[index].keys():
            # 当前层级下子主题数组
            # 每提取一次子主题，count即++一次，记录分支数量
            caseCount += 1
            topic_topics = case_topics[index]['topics']

            # 递归
            get_xmind_zen_dict(ws, topic_topics,main_topic)

        else:
            # 某一个分支遍历结束，需要做一次标记，行列需要还原

            #同层级最末分支
            level_equal_temp = len(case_topics)

            #处理行、列数值
            if  level_equal_temp > 1:
                columnIndex -= 1
                level_equal += 1

            rowIndex += 1

        #一次for循环结束后，还原
        if level_equal == feature_topic_count:
            columnIndex = columnIndex - caseCount +1



if __name__ == '__main__':
    # 用例地址
    file_path = 'Xmind转成Excel.xmind'

    # 首层画布
    xmind_origin = xmind_to_dict(file_path)

    # 用例标题
    case_title = xmind_origin[0]['topic']['title']

    # 主用例
    case_topics = xmind_origin[0]['topic']['topics']

    #需要把最外层的主题内容记录下来，以便进行匹配
    main_topic = []
    for topic in case_topics:
        main_topic.append(topic['title'])


    # 创建一个Excel文件
    wb = Workbook()
    ws = wb.active

    # 用例集遍历
    get_xmind_zen_dict(ws, case_topics,main_topic)

    # 保存Excel文档
    wb.save('test.xlsx')
