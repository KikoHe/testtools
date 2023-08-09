import openai
import base64
from PIL import Image
from io import BytesIO

openai.api_key = "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"

response = openai.Completion.create(
    engine="davinci",
    # model="davinci",
    prompt="Generate an image of a cute cat",
    size="512x512",
    format="image"
)

image_data = response.choices[0].image
image_bytes = base64.b64decode(image_data.split(',')[1])
image = Image.open(BytesIO(image_bytes))

image.show()
