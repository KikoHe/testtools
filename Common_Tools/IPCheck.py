###查询ip所属国家
import requests
ip = "34.160.187.252"
url = f"http://ip-api.com/json/{ip}"

response = requests.get(url)
data = response.json()

country = data.get("country", "Unknown")
print(f"{ip} 属于 {country}")
