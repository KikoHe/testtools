import Get_Pic, Common_Fun

def test_number_error(address,limit=10):
    # 测试范围：address素材列表中今天的素材
    # 测试内容：plan和center的元素是否一致
    ids = Get_Pic.Get_Picid(address,limit)
    failed_ids = []
    for id_ in ids:
        data = Get_Pic.Get_Zip(id_, address)
        difference = set(Get_Pic.Get_Number_From_Plan(data))-set(Get_Pic.Get_Number_From_Center(data))
        if difference:
            # raise ValueError(f"Plan中含有Center中没有的元素: {difference}")
            # failed_ids.insert(-1, id_)
            failed_ids.append(id_)
        else:
            Common_Fun.remove_zip_files_and_directories(id_)
    return failed_ids

def test_one_pic(address, PicID):
    # 测试范围：PicID
    # 测试内容：plan和center的元素是否一致
    data = Get_Pic.Get_Zip(PicID, address)
    difference = set(Get_Pic.Get_Number_From_Plan(data)) - set(Get_Pic.Get_Number_From_Center(data))
    if difference:
        raise ValueError(f"Plan中含有Center中没有的元素: {difference}")

def test_picupdate(address,limit):
    ids = Get_Pic.Get_Picid(address,limit)
    if ids == []:
        print(f"今天{address}未更新素材！！！" )
    else:
        print(f"今天{address}一共更新{len(ids)}张素材。 ")