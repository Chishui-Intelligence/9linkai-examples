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

## 能开 Code Mode 吗？

不能。Claude Code 的实验功能 Code Mode（v2.1.323 起，`CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1`）只支持直连 Anthropic 官方。客户端发现设了 `ANTHROPIC_BASE_URL` 或用 `ANTHROPIC_AUTH_TOKEN` 登录，启动时会提示：

```text
⚠ Code Mode (experimental) isn't available: for now it only works directly with
the Anthropic API (not through a cloud provider such as Bedrock, a gateway or
another address in ANTHROPIC_BASE_URL). Starting with the ordinary tools.
```

这是客户端本地的限制，所有中转都一样。开启条件、报错对照和「中转与官方账号并用」的办法见 [Claude Code 的 Code Mode 怎么开](https://9linkai.com/guide/code-mode)。
