"""用 OpenAI SDK 调 GPT（Responses API）。pip install openai；export NINELINK_API_KEY=sk-..."""
import os

from openai import OpenAI

client = OpenAI(
    base_url="https://api.9linkai.com/v1",  # OpenAI 协议：要带 /v1
    api_key=os.environ["NINELINK_API_KEY"],
)

resp = client.responses.create(model="gpt-6.1-sol", input="你好")
print(resp.output_text)
