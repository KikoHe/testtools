import requests
from bs4 import BeautifulSoup

url = "https://tx3.netease.com/forum.php?mod=viewthread&tid=1256607&page=1&authorid=578740"
headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    # 'Accept-Language': 'en-US,en;q=0.9',
    # 'referer':"https://vincent2.lexinshengwen.com/",
    # 'vincent_client_platform':'web'
}
cookies = {
    # 'cookie': '''_ga=GA1.1.1510704692.1683710635; sidebarStatus=0; uac_passport="2|1:0|10:1686638111|12:uac_passport|44:ZmU1MDA2ZTU0Y2Y1NDE5MWE4YTJmY2FmYjIwZGMzYTY=|032023a76e9d5a5bd5eb25dfb69b91592b2b6b244fd33625897ba0c750102094"; user="2|1:0|10:1686638111|4:user|1000:eyJpZCI6ICI1Yzg1YzJlZDlkZWYyYzAwMDE2MzZjNGIiLCAidXNlcmlkIjogIjE1NTIyNjk4Nzc3NDk2Mzg3IiwgImRpbmdJZCI6ICIkOkxXQ1BfdjE6JDBsMnhBNG5ELzlJTW5yMFpFZWpDeHc9PSIsICJvcGVuSWQiOiAiR1AyUWRxWm1TQ1JRV3hCU0RETlNpaXdpRWlFIiwgInVuaW9uaWQiOiAiR1AyUWRxWm1TQ1JRV3hCU0RETlNpaXdpRWlFIiwgIm1vYmlsZSI6ICIrODYtMTM5ODE3MzgwMDMiLCAidGVsIjogIiIsICJ3b3JrUGxhY2UiOiAiIiwgInJlbWFyayI6ICIiLCAib3JkZXIiOiAxNzYzNjUzNTE3Mjg1OTk1MTIsICJpc0FkbWluIjogZmFsc2UsICJpc0Jvc3MiOiBmYWxzZSwgImlzSGlkZSI6IGZhbHNlLCAiaXNMZWFkZXIiOiBmYWxzZSwgIm5hbWUiOiAiXHU0ZjU1XHU2ZDliIiwgImFjdGl2ZSI6IHRydWUsICJkZXBhcnRtZW50IjogWzYyOTI5NDcxXSwgInBvc2l0aW9uIjogIlx1NmQ0Ylx1OGJkNVx1NWRlNVx1N2EwYlx1NWUwOCIsICJlbWFpbCI6ICJoZXRhb0BkYWlseWlubm92YXRpb24uYml6IiwgImF2YXRhciI6ICJodHRwczovL3N0YXRpYy1sZWdhY3kuZGluZ3RhbGsuY29tL21lZGlhL2xBRFBEZ1E5cTl6NndPX05BYlhOQWFRXzQyMF80MzcuanBnIiwgImpvYm51bWJlciI6ICIiLCAic3RhdGVDb2RlIjogIjg2IiwgImV4dGF0dHIiOiB7fSwgImhpcmVkRGF0ZSI6IDE1NTIyMzM2MDAwMDAsICJxdWl0RGF0ZSI6IG51bGwsICJkYXRlT2ZCaXJ0aCI6ICIxOTkxLTA4LTIzIiwgImhpcmVkIjogMTU1Nn0=|6ab505f1be5ba5793e87fcc1f9037fb111d938d6be027fb08188f6c8b876d312"; _ga_2Z4PFG28RG=GS1.1.1686638103.11.1.1686638167.60.0.0'''
}
response = requests.get(url,headers=headers,cookies=cookies)
soup = BeautifulSoup(response.text,'HTML.parser')
title = soup.title.string
content = soup.select_one("#postmessage_22392429")
all_text = content.get_text(strip=True)
print(all_text)