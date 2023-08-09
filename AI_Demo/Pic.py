import openai
import requests
from requests.structures import CaseInsensitiveDict

openai.api_key = "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"

# 要生成图片的描述
description = ""

# 调用 Dall-E 模型生成图片
response = openai.Image.create(
    model="image-alpha-001",
    prompt=description,
    n=1,
    temperature=0.7,
    size="512x512"
)

# 从响应中获取图片 URL
image_url = response["data"][0]["url"]

# 从图片 URL 下载图片
headers = CaseInsensitiveDict()
headers["User-Agent"] = "Mozilla/5.0"
headers["Accept"] = "image/jpeg"

response = requests.get(image_url, headers=headers)

# 将图片保存到本地
with open("dalle_generated_image.jpg", "wb") as f:
    f.write(response.content)
