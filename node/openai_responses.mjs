// 用 OpenAI SDK 调 GPT（Responses API）。npm install openai；export NINELINK_API_KEY=sk-...
import OpenAI from 'openai'

const client = new OpenAI({
  baseURL: 'https://api.9linkai.com/v1', // OpenAI 协议：要带 /v1
  apiKey: process.env.NINELINK_API_KEY,
})

const resp = await client.responses.create({ model: 'gpt-6.1-sol', input: '你好' })
console.log(resp.output_text)
