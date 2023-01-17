import requests
'''
获取成就阶段ID
'''

headers = {
    "cookie": 'name=%E4%BD%95%E6%B6%9B; avatar=https://static-legacy.dingtalk.com/media/lADPDgQ9q9z6wO_NAbXNAaQ_420_437.jpg; uac_passport="2|1:0|10:1672277962|12:uac_passport|44:OGJmYTEzYmVhMDIyNGZhNjk1NmI4YTMxZDJmYmU2Njc=|564122050ea34481e3d7f500f059df5feeae57216fbb947bdec40d5ac4d106be"; user="2|1:0|10:1672285284|4:user|920:eyJpZCI6IjVjODVjMmVkOWRlZjJjMDAwMTYzNmM0YiIsInVzZXJpZCI6IjE1NTIyNjk4Nzc3NDk2Mzg3IiwiZGluZ0lkIjoiJDpMV0NQX3YxOiQwbDJ4QTRuRFwvOUlNbnIwWkVlakN4dz09Iiwib3BlbklkIjoiR1AyUWRxWm1TQ1JRV3hCU0RETlNpaXdpRWlFIiwidW5pb25pZCI6IkdQMlFkcVptU0NSUVd4QlNERE5TaWl3aUVpRSIsIm1vYmlsZSI6IjEzOTgxNzM4MDAzIiwidGVsIjoiIiwid29ya1BsYWNlIjoiIiwicmVtYXJrIjoiIiwib3JkZXIiOjE3NjM2NTM1MTcyODU5OTUxMiwiaXNBZG1pbiI6ZmFsc2UsImlzQm9zcyI6ZmFsc2UsImlzSGlkZSI6ZmFsc2UsImlzTGVhZGVyIjpmYWxzZSwibmFtZSI6Ilx1NGY1NVx1NmQ5YiIsImFjdGl2ZSI6dHJ1ZSwiZGVwYXJ0bWVudCI6WzYyOTI5NDcxXSwicG9zaXRpb24iOiJcdTZkNGJcdThiZDVcdTVkZTVcdTdhMGJcdTVlMDgiLCJlbWFpbCI6ImhldGFvQGRhaWx5aW5ub3ZhdGlvbi5iaXoiLCJhdmF0YXIiOiJodHRwczpcL1wvc3RhdGljLWxlZ2FjeS5kaW5ndGFsay5jb21cL21lZGlhXC9sQURQRGdROXE5ejZ3T19OQWJYTkFhUV80MjBfNDM3LmpwZyIsImpvYm51bWJlciI6IiIsInN0YXRlQ29kZSI6Ijg2IiwiZXh0YXR0ciI6e30sImhpcmVkRGF0ZSI6MTU1MjIzMzYwMDAwMCwicXVpdERhdGUiOm51bGwsImRhdGVPZkJpcnRoIjpudWxsLCJoaXJlZCI6MTM5MH0=|eb75ba8b52c299801eddffe0ba97d3d7f3910601aa420fc6d70a5e88e5fc7985"'
}
url1 = "https://cms.colorflow.app/colorflow/v1/cms/achievement/?offset=0&limit=50"
url = "https://api.colorflow.app/colorflow/v1/achievement/"
ids = ["63ad04626b6b93e813412fbb"]
# ids = [
# "607809d0e856e08099118662",
# "607809d0e856e08099118638",
# "607809d0e856e08099118623",
# "607809d0e856e0809911862a",
# "607809d0e856e080991186a8",
# "607809d0e856e08099118631",
# "63ad05b96b6b93e813413029",
# "607809d0e856e08099118654",
# "607809d0e856e0809911864d",
# "607809d0e856e08099118669",
# "607809d0e856e0809911865b",
# "607809d0e856e08099118646",
# "607809d0e856e0809911867e",
# "607809d0e856e0809911868c",
# "63ad06666b6b93e813413043",
# "607809d0e856e0809911861a"]
for m in range(len(ids)):
    id = ids[m]
    # print("ceshi"+id)
    url2 ="https://cms.colorflow.app/colorflow/v1/cms/achievement/"+id+"/stage/?offset=0&limit=50"
    response = requests.get(url2, headers=headers).json()
    data = response["data"]["content"]
    for i in range(len(data)):
        id1=data[i]["id"]
        print(id1)
