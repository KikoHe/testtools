import requests,pandas

f = pandas.read_excel("/Users/ht/Downloads/11.xlsx")
testid = f.values[:, 2]
# print(testid[0])
# print(testid[len(testid)-2])

ids1 = '+'.join(testid[0:600])
ids2 = '+'.join(testid[601:len(testid)-2])
url1 = "https://cms.colorflow.app/colorflow/v1/cms/paint?paint_id=" + ids1 + "&offset=0&limit=10000"
url2 = "https://cms.colorflow.app/colorflow/v1/cms/paint?paint_id=" + ids2 + "&offset=0&limit=10000"
headers = {
    "cookie": 'name=%E4%BD%95%E6%B6%9B; avatar=https://static-legacy.dingtalk.com/media/lADPDgQ9q9z6wO_NAbXNAaQ_420_437.jpg; _ga=GA1.1.680858957.1673418595; id=5c85c2ed9def2c0001636c4b; uac_passport="2|1:0|10:1677492832|12:uac_passport|44:NTZhNjE4YjFmMTFiNGJiYWJhNjhiYjlhZTk4YmIxMGE=|db0eb4df0fd2aa19995fa49df9615832ce4ac271dffaa95acfd8cd4c206fd2cf"; user="2|1:0|10:1677492832|4:user|936:eyJpZCI6IjVjODVjMmVkOWRlZjJjMDAwMTYzNmM0YiIsInVzZXJpZCI6IjE1NTIyNjk4Nzc3NDk2Mzg3IiwiZGluZ0lkIjoiJDpMV0NQX3YxOiQwbDJ4QTRuRFwvOUlNbnIwWkVlakN4dz09Iiwib3BlbklkIjoiR1AyUWRxWm1TQ1JRV3hCU0RETlNpaXdpRWlFIiwidW5pb25pZCI6IkdQMlFkcVptU0NSUVd4QlNERE5TaWl3aUVpRSIsIm1vYmlsZSI6Iis4Ni0xMzk4MTczODAwMyIsInRlbCI6IiIsIndvcmtQbGFjZSI6IiIsInJlbWFyayI6IiIsIm9yZGVyIjoxNzYzNjUzNTE3Mjg1OTk1MTIsImlzQWRtaW4iOmZhbHNlLCJpc0Jvc3MiOmZhbHNlLCJpc0hpZGUiOmZhbHNlLCJpc0xlYWRlciI6ZmFsc2UsIm5hbWUiOiJcdTRmNTVcdTZkOWIiLCJhY3RpdmUiOnRydWUsImRlcGFydG1lbnQiOls2MjkyOTQ3MV0sInBvc2l0aW9uIjoiXHU2ZDRiXHU4YmQ1XHU1ZGU1XHU3YTBiXHU1ZTA4IiwiZW1haWwiOiJoZXRhb0BkYWlseWlubm92YXRpb24uYml6IiwiYXZhdGFyIjoiaHR0cHM6XC9cL3N0YXRpYy1sZWdhY3kuZGluZ3RhbGsuY29tXC9tZWRpYVwvbEFEUERnUTlxOXo2d09fTkFiWE5BYVFfNDIwXzQzNy5qcGciLCJqb2JudW1iZXIiOiIiLCJzdGF0ZUNvZGUiOiI4NiIsImV4dGF0dHIiOnt9LCJoaXJlZERhdGUiOjE1NTIyMzM2MDAwMDAsInF1aXREYXRlIjpudWxsLCJkYXRlT2ZCaXJ0aCI6IjE5OTEtMDgtMjMiLCJoaXJlZCI6MTQ1MH0=|4bd1a7349ebd98622042956c984d38f0ef6ae7ad34c29031c56c7d00af81191d"; _ga_2Z4PFG28RG=GS1.1.1677492826.23.1.1677492837.49.0.0'
}
response = requests.get(url1, headers=headers).json()
paint_list = response["data"]["paint_list"]
for i in range(len(paint_list)):
    related_id = paint_list[i]["related_id"][0]
    material_number = paint_list[i]["detail"][0]["material_number"]
    if material_number == None:
        print(related_id)

