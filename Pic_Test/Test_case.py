from Get_zip_data import *
from Get_pic_data_from_api import *
import multiprocessing
from Common_Fun import *

folder_path = '/Users/ht/Desktop/PythonTools/Pic_Test/Pic/'
if os.path.exists(folder_path):
    delete_folder(folder_path)

# 测试单张素材（SVG + PDF）
def test_single_pic(PicID, address):
    not_svg_zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(PicID, address)
    get_zip_detail(address, PicID, not_svg_zip_url)
    not_svg_test_result = test_zip_data(address, PicID)
    if svg_zip_url != '':
        get_zip_detail(address, PicID, svg_zip_url)
        svg_test_result = check_svg_by_cmd(PicID)
    else:
        svg_test_result = True
    if not_svg_test_result == False or svg_test_result == False:
        return False
    else:
        return True

# 测试单张素材（SVG）
def test_single_pic_svg(PicID, address):
    not_svg_zip_url, svg_zip_url = Get_id_Zipurl_from_picdetailapi(PicID, address)
    svg_test_result = True
    if svg_zip_url != '':
        get_zip_detail(address, PicID, svg_zip_url)
        svg_test_result = check_svg_by_cmd(PicID)
    return svg_test_result

# 测试明天更新的素材（通过一张一张的请求素材详情的数据,包括SVG+PDF）
def test_update_pic_single_by_single(address_input=''):
    test_result = []
    fail_groups = []
    fail_ids = []
    if address_input == '':
        address_list = ["PBN_Lib", "PBN_Daily", "PBN_Story", "ZC_Lib", "ZC_Daily", "VC_Lib", "VC_Daily",\
                        "Vista_Lib", "Vista_Daily", "Vista_Pack", "BP_Lib", "BP_Daily"]
    else:
        address_list = [address_input]
    for address in address_list:
        print("开始测试项目模块:"+str(address))
        if address == "PBN_Story":
            pid_ids = get_today_uptate_story_pic_id()
        elif address == "Vista_Pack":
            pid_ids = get_today_update_pack_pic_id()
        else:
            pid_ids, fail_groups = get_all_imagegroup_pic_update(address)

        for pic_id in pid_ids:
            print("开始测试素材:" + str(pic_id))
            test_zip_data_result_pdf = test_single_pic(pic_id, address)
            if test_zip_data_result_pdf == False:
                print("资源测试异常的素材ID： " + str(pic_id))
                fail_ids.append(pic_id)

        update_pic_number = len(pid_ids)

        test_result_single_project = {address: [update_pic_number, fail_ids, fail_groups]}
        test_result.append(test_result_single_project)
    return test_result

# 通过CMS接口拉取测试素材，通过单素材接口获取测试资源（SVG+PDF）
# 要调整拉取范围，需要修改pic_config中的url即可
def test_pic_from_cms(address="PBN",offset=0,limit=100):
    id_list = pic_config(address, offset, limit)
    ids = list(id_list.keys())
    print("总测试素材数" + str(len(ids)))
    fail_ids = []
    i = 1
    for PicID in ids:
        print(f"第{i}个测试素材，ID： {PicID}")
        test_zip_data_result = test_single_pic(PicID, address)
        # test_zip_data_result = test_single_pic_svg(PicID, address)
        if test_zip_data_result == False:
            fail_ids.append(PicID)
            print("截止目前所有异常的素材ID： " + str(fail_ids))
            output = "测试结果：" + str(PicID) + "\n"
            with open(f'output_{offset}.txt', 'a') as file:
                file.write(output)  # 写入输出结果到文件中
        i = i + 1
    return fail_ids
# 多任务同时执行
def multi_action_test():
    address = "PBN"
    offsets = [20000, 21000, 22000, 23000, 24000]
    args = [(address, offset) for offset in offsets]
    with multiprocessing.Pool() as pool:
        pool.map(test_pic_from_cms, args)

# 读取本地文件中的ID，分开输出number异常和不是number异常的素材ID
# 文件和脚本在同一个目录
def dist_error_id(filename):
    current_dir = os.getcwd()
    file = current_dir + '/' + filename
    address = "PBN"
    number_fail_ids = []
    with open(file, 'r') as f:
        content = f.read()
        content = content.strip().split('\n')
        for PicID in content:
            test_zip_data_result = test_single_pic_svg(PicID, address)
            if test_zip_data_result != None:
                number_fail_ids.append(test_zip_data_result)
        not_number_fail_ids = [x for x in content if x not in number_fail_ids]
    return number_fail_ids, not_number_fail_ids
# ids = ['652d006b20e621eaa7fa0ce9', '65277d26bcf5a38b83c6075d', '650829cae7da2c97ed517b77', '6515294c15611057689f6db7', '6512ab0b0f45d2f166c677c9', '650be8c91aeceec6238cf9d6', '650ab1a31aeceec6238ce100', '65000bb2ebbba5ca7147e485', '64ffd50bdf9df0808ce21d8f', '63e4b86cd32ec78307fbb7f2', '63e4b8340d8cc00bb06e46cb', '63e0d5f4f64100f35cca4884', '63b54b5f42a16e6634cd2de2', '63b3f7a3b88e7f18d01fa65a', '647dcbe88a5d5cb6ce516100', '647dcbe88a5d5cb6ce5160ff', '6476fd245ebea2f1646962f5', '6476fd245ebea2f1646962ed', '64704bc02fa7983029a71ca1', '64703348d4ff69182635b573', '6466e57750b3c1f592e72f1a', '6462179ddd72017db672d760', '645cc6db72617f5aa3a7cc5f', '645c8edef401515f46dcf51d', '64426273076396aa13e1218f', '64410fda9bd78f4e6031bfd1', '643fbc13379a34e0fae742ca', '643e621ac0830c8b478ef8b0', '638dbc678bbc0a11d3226a97', '6373616538da466fbbc0edfa', '65d2d3e2a64b6582fe05694b', '65d2d41473358196a167723f', '65d2d3e2a64b6582fe05692c', '65d2d3e2a64b6582fe056923', '65c1e98173358196a1671ebd', '65c0809973358196a166ef5f', '65bcbde9a64b6582fe048c51', '65bcbde9a64b6582fe048c63', '65bb2fa5a64b6582fe0459c2', '65b34bc2a64b6582fe03a7fd', '65b1e243a64b6582fe037ba3', '65add900a64b6582fe02f570', '65a5fd23f4f3a2c24893f5d1', '659cc867d0e2d694fbb0d649', '6593aacff7855ed937407740', '65938a13f7855ed937407427', '658e5405ae17e22bc123b7d1', '664da088471231ae29f0a0fe', '6642dd47fa9fdef935383b1a', '663b00078a97705c86b8b1ff', '662a06c07dd503c70a03d519', '662764fe4f375dad5d78bc6b', '65852a56212d347aeb207d3a', '657a8300c14c58ea92aeac88', '656584eb400a2d4b3a0f2e68', '6556fd1d61b9c94253ec31df', '6555bfdd74cd8604b3603f7f', '654c5afa61b9c94253eb894c', '654b165561b9c94253eb7161', '6437d382054e2714da616902', '642e97b12cbe8d93b896e18f', '642a9e2d30126482275193e9', '642a9e2d30126482275193e6', '642a9e2d30126482275193d3', '6426a83d75789727894e8805', '64182c00d5d4a09c2b6928cd', '6410437bbb9cffd1306b41ba', '640eefe526dea6d7e461da33', '63bfe5b63c6b306bad570c71', '63f5e359530c3bd9785385af', '63ef4967af7d576d8b1f3b02', '64df15f18bbeb4103bd087d1', '64d367d003e5ec12ac2bea56', '64d0d56b7619a9f15201fece', '64d0ccfa7619a9f15201fc44', '64cb08584fdf73580190b7a0', '64c8b5c9cf2980846459c154', '64bf6e7fb0467fd3eceb0ccf', '64b8e29583f06cbac22ff91b', '64b8e29583f06cbac22ff910', '64ab80ad36af7ba8feef0029', '6492dff888770adc70366ae0', '661e28e64f375dad5d77b2c8', '661ccab94f375dad5d7771df', '6614f8c7167c11dcc35980ef', '65e6b80ba9e57ea1e24cc755', '66050baa27615e227cfa15bc', '65fd1c6a48defc641251e6f4', '65f2e7d0296812e63bf122ab', '65f000298aaea5115b2c1d4e', '65ee958e9b5ba646dd954c8e', '668e77da47888354fffdde6a', '668764d5cd6bcc4ded4f1af4', '666a96475f0e3caf41f7a457']
# ids = ['657a8300c14c58ea92aeac88']
# # ids = ['64ffd50bdf9df0808ce21d8f', '63e4b86cd32ec78307fbb7f2', '63e4b8340d8cc00bb06e46cb', '63e0d5f4f64100f35cca4884', '63b54b5f42a16e6634cd2de2', '63b3f7a3b88e7f18d01fa65a', '64426273076396aa13e1218f', '638dbc678bbc0a11d3226a97', '6373616538da466fbbc0edfa', '65d2d3e2a64b6582fe05694b', '65bb2fa5a64b6582fe0459c2', '65add900a64b6582fe02f570', '659cc867d0e2d694fbb0d649', '65938a13f7855ed937407427', '658e5405ae17e22bc123b7d1', '657a8300c14c58ea92aeac88', '656584eb400a2d4b3a0f2e68', '6556fd1d61b9c94253ec31df', '654c5afa61b9c94253eb894c', '654b165561b9c94253eb7161', '6437d382054e2714da616902', '63bfe5b63c6b306bad570c71', '63f5e359530c3bd9785385af', '63ef4967af7d576d8b1f3b02', '64d367d003e5ec12ac2bea56', '64d0ccfa7619a9f15201fc44', '64c8b5c9cf2980846459c154', '64bf6e7fb0467fd3eceb0ccf', '65fd1c6a48defc641251e6f4', '65f2e7d0296812e63bf122ab', '65ee958e9b5ba646dd954c8e', '668764d5cd6bcc4ded4f1af4']
# error_ids = []
# for id in ids:
#     print(id)
#     test_result = test_single_pic_svg(id, "PBN")
#     if test_result == False:
#         error_ids.append(id)
# print("error!!!!!!!!!!"+str(error_ids))
