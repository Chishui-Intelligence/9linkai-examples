# Codex CLI

1. 把 [`config.toml`](config.toml) 复制到 `~/.codex/config.toml`（已有文件先备份）。
2. 设置 Key 并启动：

```bash
export OPENAI_API_KEY="sk-你的密钥"   # Windows PowerShell：$env:OPENAI_API_KEY="sk-你的密钥"
codex
```

久连 9LinkAI 支持 Codex 需要的 Responses API（`/v1/responses`）。

常见坑：

1. `base_url` 写到 `/v1` 为止，不要写成 `/v1/responses`。
2. `model_provider` 只认用户目录下的 `~/.codex/config.toml`，写在项目里的 `.codex/config.toml` 会被忽略。
3. provider 名字不要用 `openai`、`ollama`、`lmstudio`（Codex 内置保留名）。
