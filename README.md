# 久连 9LinkAI 接入示例

[久连 9LinkAI](https://9linkai.com)（9Link）是 Claude 与 GPT 官方模型的 API 中转平台：一个 API Key 接入 Anthropic 与 OpenAI 的官方模型，按官方公开价 6 折、按实际用量计费，兼容 Claude Code 和 Codex CLI。

本仓库收集各种工具和 SDK 的**复制即用配置**，以及一个**自助验真脚本**。

> 久连 9LinkAI 是独立的第三方服务，与 Anthropic、OpenAI 均无隶属关系；也与 LinkAI（link-ai.tech）、linkai.shop 没有任何关联。

## 接口地址

| 协议 | Base URL | 用于 |
|---|---|---|
| Anthropic | `https://api.9linkai.com`（不带 /v1） | Claude Code、Anthropic SDK、Cline（Anthropic 提供商） |
| OpenAI | `https://api.9linkai.com/v1` | Codex CLI（Responses API）、OpenAI SDK、Cursor、Cline（OpenAI Compatible） |

API Key 在[控制台](https://9linkai.com)创建，可用模型和价格见[模型广场](https://9linkai.com/model-plaza)。

## 目录

| 目录 | 内容 |
|---|---|
| [`claude-code/`](claude-code) | `settings.json` 与环境变量写法（macOS / Linux / Windows） |
| [`codex/`](codex) | `~/.codex/config.toml`，默认模型 `gpt-6.1-sol` |
| [`python/`](python) | Anthropic SDK 基础调用、提示词缓存；OpenAI SDK Responses API |
| [`node/`](node) | OpenAI SDK（Responses API） |
| [`curl/`](curl) | 三条命令测试 Key 是否可用 |
| [`verify/`](verify) | 自助验真脚本：原生响应结构、缓存、流式事件、Responses API |

## 30 秒上手

### Claude Code

```bash
export ANTHROPIC_BASE_URL="https://api.9linkai.com"
export ANTHROPIC_AUTH_TOKEN="sk-你的密钥"
claude
```

### Codex CLI

把 [`codex/config.toml`](codex/config.toml) 复制到 `~/.codex/config.toml`，然后：

```bash
export OPENAI_API_KEY="sk-你的密钥"
codex
```

## 计费

- 久连价 = 官方公开价 × 6 折，缓存读写同折扣，随官方调价同步
- 输入、输出、缓存写入、缓存读取分项计费，每一笔调用都能在控制台逐笔查询
- 余额以人民币计价（1 美元 = 6.90 元），充值无最低额；未消费的实付金额可申请退款

## 常见问题

- **地址要不要带 /v1？** Anthropic 协议不带，OpenAI 协议要带。写反会报 404。
- **报 401？** Key 填错或前后多了空格；先用 [`curl/test.sh`](curl/test.sh) 单独验证。
- **报 404 model_not_found？** 模型名写错，或者 Key 所在分组没有这个模型；用 `GET /v1/models` 查看可用模型。

更多说明见[使用指南](https://9linkai.com/guide)和[错误码说明](https://9linkai.com/errors)。

## License

MIT
