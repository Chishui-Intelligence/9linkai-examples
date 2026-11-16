# Claude Code

把 [`settings.json`](settings.json) 的 `env` 段合并进 `~/.claude/settings.json`（Windows：`%USERPROFILE%\.claude\settings.json`），所有终端和 IDE 插件都会生效。

只想在当前终端试用：

```bash
# macOS / Linux
export ANTHROPIC_BASE_URL="https://api.9linkai.com"
export ANTHROPIC_AUTH_TOKEN="sk-你的密钥"
claude
```

```powershell
# Windows PowerShell
$env:ANTHROPIC_BASE_URL="https://api.9linkai.com"
$env:ANTHROPIC_AUTH_TOKEN="sk-你的密钥"
claude
```

常见坑：

1. 地址**不要**带 `/v1`，Claude Code 会自己拼 `/v1/messages`。
2. IDE 插件读不到终端里临时 `export` 的变量，用 settings.json 或完全重启 IDE。
3. 只保留 `ANTHROPIC_AUTH_TOKEN`；之前为别的服务设过的 `ANTHROPIC_API_KEY` 要删掉。
