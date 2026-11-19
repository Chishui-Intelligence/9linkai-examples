# 自助验真

```bash
NINELINK_CLAUDE_KEY=sk-... NINELINK_OPENAI_KEY=sk-... python3 verify.py
```

检查其他网关或中转（根地址，不带 `/v1`）：

```bash
VERIFY_BASE_URL=https://your-gateway.example.com NINELINK_CLAUDE_KEY=sk-... NINELINK_OPENAI_KEY=sk-... python3 verify.py
```

## English

A zero-dependency script that checks whether an Anthropic/OpenAI-compatible gateway behaves like the official APIs: native `msg_` message IDs, prompt-cache usage fields (`cache_creation_input_tokens` / `cache_read_input_tokens`), native streaming event order, signed thinking blocks, and the `/v1/responses` endpoint that Codex CLI requires. Set `VERIFY_BASE_URL` to the gateway root (without `/v1`).

检查项：

1. **原生响应结构**：`id` 以 `msg_` 开头，`type` 为 `message`
2. **提示词缓存**：同一前缀连发两次，第二次 `usage` 里有 `cache_read_input_tokens`
3. **原生流式事件**：`message_start` → `content_block_*` → `message_delta` → `message_stop`
4. **思考块与签名**：adaptive thinking 返回带 `signature` 的 thinking 块
5. **Responses API**：Codex 依赖的 `/v1/responses` 接口

只用 Python 标准库，不需要安装依赖。建议用专门建的低额度 Key，测完删掉。
