"""Claude 提示词缓存：连续请求两次，第二次的 usage 里能看到 cache_read_input_tokens。"""
import os

import anthropic

client = anthropic.Anthropic(base_url="https://api.9linkai.com", api_key=os.environ["NINELINK_API_KEY"])

# 缓存的内容太短不会生效（通常至少 1024 个 token），这里用一段长文本演示
document = "这是一份需要反复引用的长文档。" * 400

for i in (1, 2):
    msg = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=64,
        system=[{
            "type": "text",
            "text": document,
            "cache_control": {"type": "ephemeral"},  # 想缓存 1 小时：{"type": "ephemeral", "ttl": "1h"}
        }],
        messages=[{"role": "user", "content": "用一句话概括这份文档"}],
    )
    u = msg.usage
    print(f"第 {i} 次：写入缓存 {u.cache_creation_input_tokens}，读取缓存 {u.cache_read_input_tokens}")
