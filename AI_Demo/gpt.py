import requests

# 替换为你的 API 密钥
API_KEY = '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'

def chat_gpt(prompt):
    url = 'https://api.openai.com/v1/engines/text-davinci-002/completions'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
    }

    data = {
        'prompt': prompt,
        'max_tokens': 100,  # 设定生成回复内容的最大长度
        'temperature': 0.5,  # 控制输出随机性 (0-1之间, 取值越高结果越随机)
        'n': 1,  # 请求生成回复的数量
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if response.status_code == 200:
        message = result['choices'][0]['text'].strip()
        return message
    else:
        print(f"Error {response.status_code}: {result}")
        return None


if __name__ == '__main__':
    prompt_text = 'What is the capital of France?'
    generated_text = chat_gpt(prompt_text)
    print(f"Generated text: {generated_text}")

