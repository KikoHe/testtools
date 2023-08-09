import openai

openai.api_key = "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"
models = openai.Model.list()

# print the first model's id
print(models)
#
# # 创建一个新模型
# model = openai.Model.create(
#     engine="davinci",  # 选择模型引擎
#     name="kiko-pic-001",   # 设置模型名称
#     prompt="This is a test prompt"  # 设置测试 prompt
# )
#
# # 输出模型 ID 和 API 密钥
# print("Model ID: ", model.id)
# print("API Key: ", model.private_key)

