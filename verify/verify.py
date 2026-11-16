"""久连 9LinkAI 自助验真：检查官方接口才有的协议特征。只用 Python 标准库。

    NINELINK_CLAUDE_KEY=sk-... NINELINK_OPENAI_KEY=sk-... python3 verify.py

两个 Key 可以是同一个（如果你的分组同时有 Claude 和 GPT）。只设其中一个时，另一类检查会跳过。
整套检查大约消耗几毛钱。建议用一个专门建的、额度很低的 Key，测完删掉。
"""
import json
import os
import urllib.error
import urllib.request

BASE = "https://api.9linkai.com"
CLAUDE_KEY = os.environ.get("NINELINK_CLAUDE_KEY", "")
OPENAI_KEY = os.environ.get("NINELINK_OPENAI_KEY", "")
CLAUDE_MODEL = os.environ.get("NINELINK_CLAUDE_MODEL", "claude-sonnet-5-5")
GPT_MODEL = os.environ.get("NINELINK_GPT_MODEL", "gpt-6.1-sol")


def post(path, body, key, anthropic=True, raw=False):
    headers = {"content-type": "application/json"}
    if anthropic:
        headers.update({"x-api-key": key, "anthropic-version": "2023-06-01"})
    else:
        headers["authorization"] = "Bearer " + key
    req = urllib.request.Request(BASE + path, json.dumps(body).encode(), headers)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            text = r.read().decode()
            return r.status, text if raw else json.loads(text)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:300]


def report(name, ok, detail):
    print(f"[{'通过' if ok else '未通过'}] {name}：{detail}")


def check_claude():
    # 1. 原生响应结构
    s, r = post("/v1/messages", {"model": CLAUDE_MODEL, "max_tokens": 32,
                                 "messages": [{"role": "user", "content": "只回复：好"}]}, CLAUDE_KEY)
    if s != 200:
        return report("原生响应结构", False, f"HTTP {s} {r}")
    report("原生响应结构", r["id"].startswith("msg_") and r["type"] == "message",
           f"id={r['id'][:12]}… type={r['type']} stop_reason={r['stop_reason']}")

    # 2. 提示词缓存：同一段长前缀连发两次，第二次应读到缓存
    doc = "久连 9LinkAI 自助验真缓存测试文档。" * 400
    body = {"model": CLAUDE_MODEL, "max_tokens": 16,
            "system": [{"type": "text", "text": doc, "cache_control": {"type": "ephemeral"}}],
            "messages": [{"role": "user", "content": "只回复：好"}]}
    usages = []
    for _ in range(2):
        s, r = post("/v1/messages", body, CLAUDE_KEY)
        usages.append(r.get("usage", {}) if s == 200 else {})
    created = usages[0].get("cache_creation_input_tokens", 0) + usages[0].get("cache_read_input_tokens", 0)
    read = usages[1].get("cache_read_input_tokens", 0)
    report("提示词缓存", created > 0 and read > 0, f"第 1 次写入或读取 {created}，第 2 次读取 {read}")

    # 3. 原生流式事件
    s, text = post("/v1/messages", {"model": CLAUDE_MODEL, "max_tokens": 32, "stream": True,
                                    "messages": [{"role": "user", "content": "数到三"}]}, CLAUDE_KEY, raw=True)
    events = [l[6:].strip() for l in text.splitlines() if l.startswith("event:")] if s == 200 else []
    need = ["message_start", "content_block_start", "content_block_delta", "content_block_stop", "message_delta", "message_stop"]
    report("原生流式事件", all(n in events for n in need), " → ".join(dict.fromkeys(events)) or f"HTTP {s}")

    # 4. 思考块与签名（Sonnet 5.5 / Opus 5.5 用 adaptive thinking）
    s, r = post("/v1/messages", {"model": CLAUDE_MODEL, "max_tokens": 4000, "thinking": {"type": "adaptive"},
                                 "messages": [{"role": "user", "content": "仔细推理：1 到 2026 中有多少个数能被 5 整除但不能被 3 或 7 整除？"}]},
                CLAUDE_KEY)
    blocks = r.get("content", []) if s == 200 else []
    sig = next((b.get("signature", "") for b in blocks if b.get("type") == "thinking"), "")
    report("思考块与签名", bool(sig), f"签名长度 {len(sig)}" if sig else f"HTTP {s}，没有返回 thinking 块")


def check_openai():
    s, r = post("/v1/responses", {"model": GPT_MODEL, "input": "只回复：好"}, OPENAI_KEY, anthropic=False)
    if s != 200:
        return report("Responses API（Codex 用）", False, f"HTTP {s} {r}")
    report("Responses API（Codex 用）", r.get("object") == "response",
           f"object={r.get('object')} id={str(r.get('id'))[:10]}… model={r.get('model')}")


if __name__ == "__main__":
    if not CLAUDE_KEY and not OPENAI_KEY:
        raise SystemExit("请先设置 NINELINK_CLAUDE_KEY 或 NINELINK_OPENAI_KEY")
    if CLAUDE_KEY:
        check_claude()
    if OPENAI_KEY:
        check_openai()
    print("\n说明：这些检查证明的是协议特征，不能证明以后每一次请求都一样。网关会自动剥掉签名无效的思考块再重试，"
          "所以「篡改签名应报 400」这类检测不适用。详见 https://9linkai.com/guide")
