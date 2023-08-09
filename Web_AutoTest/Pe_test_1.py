import requests
from bs4 import BeautifulSoup

url = "https://vincent2.lexinshengwen.com/vincent/v1/group"
headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'referer':"https://vincent2.lexinshengwen.com/",
    'vincent_client_platform':'web'
}
cookies = {
    'cookie': '_ga=GA1.1.1510704692.1683710635; uac_passport="2|1:0|10:1686556468|12:uac_passport|44:MThjNWY3MDU0ZGZlNDQ3YWEzZmU1ZjE5ZWJlYTMzNmQ=|1c409b47ec8f4bf9f2f69afb4f08701fecff342ab74d0e57f4913f41fd488718"; user="2|1:0|10:1686556468|4:user|1000:eyJpZCI6ICI1Yzg1YzJlZDlkZWYyYzAwMDE2MzZjNGIiLCAidXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgImRpbmdJZCI6ICIkOkxXQ1BfdjE6JDBsMnhBNG5ELzlJTW5yMFpFZWpDeHc9PSIsICJvcGVuSWQiOiAiR1AyUWRxWm1TQ1JRV3hCU0RETlNpaXdpRWlFIiwgInVuaW9uaWQiOiAiR1AyUWRxWm1TQ1JRV3hCU0RETlNpaXdpRWlFIiwgIm1vYmlsZSI6ICIrODYtMTM5ODE3MzgwMDMiLCAidGVsIjogIiIsICJ3b3JrUGxhY2UiOiAiIiwgInJlbWFyayI6ICIiLCAib3JkZXIiOiAxNzYzNjUzNTE3Mjg1OTk1MTIsICJpc0FkbWluIjogZmFsc2UsICJpc0Jvc3MiOiBmYWxzZSwgImlzSGlkZSI6IGZhbHNlLCAiaXNMZWFkZXIiOiBmYWxzZSwgIm5hbWUiOiAiXHU0ZjU1XHU2ZDliIiwgImFjdGl2ZSI6IHRydWUsICJkZXBhcnRtZW50IjogWzYyOTI5NDcxXSwgInBvc2l0aW9uIjogIlx1NmQ0Ylx1OGJkNVx1NWRlNVx1N2EwYlx1NWUwOCIsICJlbWFpbCI6ICJoZXRhb0BkYWlseWlubm92YXRpb24uYml6IiwgImF2YXRhciI6ICJodHRwczovL3N0YXRpYy1sZWdhY3kuZGluZ3RhbGsuY29tL21lZGlhL2xBRFBEZ1E5cTl6NndPX05BYlhOQWFRXzQyMF80MzcuanBnIiwgImpvYm51bWJlciI6ICIiLCAic3RhdGVDb2RlIjogIjg2IiwgImV4dGF0dHIiOiB7fSwgImhpcmVkRGF0ZSI6IDE1NTIyMzM2MDAwMDAsICJxdWl0RGF0ZSI6IG51bGwsICJkYXRlT2ZCaXJ0aCI6ICIxOTkxLTA4LTIzIiwgImhpcmVkIjogMTU1NX0=|31c231971c6a1897fd647af8a236c4c7c5f3f776b35232d16761615ac6861eee"; sidebarStatus=0; _ga_2Z4PFG28RG=GS1.1.1686556462.9.1.1686556594.60.0.0 '

}
response = requests.get(url,headers=headers,cookies=cookies)
# soup = BeautifulSoup(response.text,'HTML.parser')
first_name = response.json()["data"]["groupList"][0]["name"]
# first_name_text = first_name.get_text()
print(first_name)