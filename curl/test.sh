#!/usr/bin/env bash
# 测试久连 9LinkAI 的 API Key：NINELINK_API_KEY=sk-... bash test.sh
set -euo pipefail
: "${NINELINK_API_KEY:?先设置 NINELINK_API_KEY}"
BASE=https://api.9linkai.com

echo "== 1. 这个 Key 能用的模型"
curl -sS "$BASE/v1/models" -H "Authorization: Bearer $NINELINK_API_KEY"; echo

echo "== 2. Anthropic 格式调 Claude"
curl -sS "$BASE/v1/messages" \
  -H "x-api-key: $NINELINK_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-5-5","max_tokens":64,"messages":[{"role":"user","content":"你好"}]}'; echo

echo "== 3. OpenAI 格式调 GPT（Responses API）"
curl -sS "$BASE/v1/responses" \
  -H "Authorization: Bearer $NINELINK_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model":"gpt-6.1-sol","input":"你好"}'; echo
