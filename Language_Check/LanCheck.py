import os, openpyxl,argparse
from openpyxl.styles import NamedStyle, Font, Border, Side, PatternFill, colors
from openpyxl.comments import Comment

'''检查多语言文档格式是否正确'''
# 从xlutils模块中导入copy这个函数

def updateExcel(file_path,x,y):
    '''''
    读取excel测试用例的函数
    :param file_path:传入一个excel文件，或者文件的绝对路径
    '''
    try:
        book = openpyxl.load_workbook(file_path)
    except Exception as e:
        # 如果路径不在或者excel不正确，返回报错信息
        print('路径不在或者excel不正确', e)
        return e
    else:
        sheet = book.active  # 取第一个sheet页
        rows_num = sheet.max_row + 1  # 取这个sheet页的所有行数
        clos_num = sheet.max_column + 1
        for r in list(range(rows_num))[x:]:  # 取第4行到最后一行
            for c in list(range(clos_num))[y:]:  # 取第9列到最后一行
                b = sheet.cell(row=r, column=c)
                a = b.value

                ##检查是否有内容为空###
                if a == None:
                    commentexcel(b, r, c, '内容为空')
                    continue

                # ###检查内容是否超出字符数###
                # length = sheet.cell(row=r, column=8).value
                # try:
                #     float(length)
                # except:
                #     print("跳过" + str(r) + '行' + str(c) + '列')
                # else:
                #     if len(str(a)) > int(length):
                #         commentexcel(b, r, c, '超出预定字符')

                ###检查是否有多余的空格###
                word = a.split(' ')
                for i in list(range(len(word))):
                    if word[i] == "":
                        commentexcel(b, r, c, '有多余空格')
                        break

                ###检查%的输入法问题：不能出现中文格式的%
                if a.find("％") != -1:
                    commentexcel(b, r, c, '"%"格式为中文')

                ###检查%S的大小写问题：不能出现大写的%S
                if a.find("%S") != -1:
                    commentexcel(b, r, c, '"%S"大小写错误')
                elif a.find("% S") != -1:
                    commentexcel(b, r, c, '"%S"大小写错误')

                ###检查%前后空格：%前后不能都为空格
                if a.find("%") != -1:
                    number = a.index("%")
                    if number < len(a) - 1:
                        if a[number - 1] == " " and a[number + 1] == " ":
                            commentexcel(b, r, c, '"%"前后都为空')
                    elif number == len(a) - 1 and number != 0:
                        if a[number - 1] == " ":
                            commentexcel(b, r, c, '"%"前后都为空')
                    elif number == 0 and len(a) != 1:
                        if a[number + 1] == " ":
                            commentexcel(b, r, c, '"%"前后都为空')
                    elif number == 0 and len(a) == 1:
                        commentexcel(b, r, c, '"%"前后都为空')

                ###检查"/n"前后是否有空格：/n前后不能都为空格
                if a.find("/n") != -1:
                    if a.find(" /n") != -1 or a.find("/n ") != -1:
                        commentexcel(b, r, c, '"/n"前后有空格')

                ###检查"$"后是否有空格：$前后不能都为空格
                if a.find("$") != -1:
                    if a.find(" $s") != -1:
                        commentexcel(b, r, c, '"$"后有空格/"$s"前边有空格')
                    elif a.find("$ ") != -1:
                        commentexcel(b, r, c, '"$"后有空格/"$s"前边有空格')
                        commentexcel(b, r, c, '"$"后有空格/"$s"前边有空格')
                    elif a.find("% ") != -1:
                        commentexcel(b, r, c, '"%"后有空格')

                ###检查非中文语系是否有中文标点符号
                language = sheet.cell(row=3, column=c).value
                if language != "zh-CN" and language != "zh-TW" and language != "ja":
                    if a.find("！") != -1:
                        commentexcel(b, r, c, '"！"是中文标点')
                    elif a.find("。") != -1:
                        commentexcel(b, r, c, '"。"是中文标点')
                    elif a.find("，") != -1:
                        commentexcel(b, r, c, '"，"是中文标点')
                    elif a.find("？") != -1:
                        commentexcel(b, r, c, '"？"是中文标点')
                    elif a.find("：") != -1:
                        commentexcel(b, r, c, '"："是中文标点')
                    elif a.find("（") != -1:
                        commentexcel(b, r, c, '"（"是中文标点')
                    elif a.find("）") != -1:
                        commentexcel(b, r, c, '"）"是中文标点')
                    # elif a.find("'") != -1:
                    #     commentexcel(b, r, c, '"""是中文标点')
                    # elif a.find("'") != -1:
                    #     commentexcel(b, r, c, '"""是中文标点')
                else: ###检查中文语系是否有英文标点符号
                    if a.find("!") != -1:
                        commentexcel(b, r, c, '"!"是英文标点')
                    elif a.find(",") != -1:
                        commentexcel(b, r, c, '","是英文标点')
                    elif a.find("?") != -1:
                        commentexcel(b, r, c, '"?"是英文标点')
                    elif a.find(":") != -1:
                        commentexcel(b, r, c, '":"是英文标点')
                    elif a.find("(") != -1:
                        commentexcel(b, r, c, '"("是英文标点')
                    elif a.find(")") != -1:
                        commentexcel(b, r, c, '")"是英文标点')
                    elif a.find('"') != -1:
                        commentexcel(b, r, c, '"是英文标点')

                ###检查特殊符号是否遗漏
                d = sheet.cell(row=r, column=9).value
                if d != None:
                    if d.find("%") != -1:
                        if a.find("%") == -1:
                            commentexcel(b, r, c, '缺少特殊字符"%"')
                if d.find("%s") != -1:
                    if a.find("%s") == -1:
                        commentexcel(b, r, c, '缺少特殊字符"%s"')
                if d.find("#") != -1:
                    if a.find("#") == -1:
                        commentexcel(b, r, c, '缺少特殊字符"#"')
                if d.find("$") != -1:
                    if a.find("$") == -1:
                        commentexcel(b, r, c, '缺少特殊字符"$"')
                if d.find("$s") != -1:
                    if a.find("$s") == -1:
                        commentexcel(b, r, c, '缺少特殊字符"$s"')
                if d.find("/n") != -1:
                    if a.find("/n") == -1:
                        commentexcel(b, r, c, '缺少特殊字符"/n"')
                else:
                    continue
        book.save(file_path)


def commentexcel(b, r, c, string):
    fill_3 = PatternFill("solid", fgColor="ffc7ce")  # 红色
    comment = Comment(string, "tester")

    b.fill = fill_3
    b.comment = comment
    print(str(r) + '行' + str(c) + '列' + string)
    return

###直接在代码中修改执行文件路径
# # 获取项目路径
# project_path = os.path.abspath(os.path.join(os.path.dirname(os.path.split(os.path.realpath(__file__))[0]), '.'))
#
# # 测试表格存放路径
# test_cases_path = project_path + "/Language_Check/"
#
# # 执行
# updateExcel(test_cases_path + "pbn的副本.xlsx")
parser = argparse.ArgumentParser(description='检查多语言文档格式是否正确')
parser.add_argument('file', type=str, help='检测文件路径')
parser.add_argument('row', type=int, help='从第x行开始检测')
parser.add_argument('clos', type=int, help='从第y列开始检查')
args = parser.parse_args()

# 获取文件路径参数
file_path = args.file
x = args.row
y = args.clos

# 检查文件格式
updateExcel(file_path,x,y)