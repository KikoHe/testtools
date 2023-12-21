import Get_Pic, Common_Fun

def test_number_error():
    #Plan = Center
    Project = "PBN"
    limit = 1000
    ids = Get_Pic.Get_Picid(Project,limit)
    failed_ids = []
    for id_ in ids:
            data = Get_Pic.Get_Zip(id_, Project)
            if sorted(Get_Pic.Get_Number_From_Center(data)) != sorted(Get_Pic.Get_Number_From_Plan(data)):
                failed_ids.insert(-1, id_)
            continue