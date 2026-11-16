"""用 Anthropic SDK 调 Claude。pip install anthropic；export NINELINK_API_KEY=sk-..."""
import os

import anthropic

client = anthropic.Anthropic(
    base_url="https://api.9linkai.com",  # Anthropic 协议：不带 /v1
    api_key=os.environ["NINELINK_API_KEY"],
)

msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "你好"}],
)
print(msg.content[0].text)
print(msg.usage)
