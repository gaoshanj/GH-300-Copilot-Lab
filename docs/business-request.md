# 业务需求：生成文本校验和 API

新增一个 API Endpoint，接收文本 Payload，并返回确定性的 checksum（校验和）。

## 验收标准 Acceptance criteria

- `POST /checksum` 接收 JSON，必须包含 `text` 字段。
- 空文本必须返回 HTTP 422。
- 响应必须包含名为 `checksum` 的整数值。
- 相同输入必须始终产生相同输出。
- 输入长度限制为 10,000 个字符。
- 增加正常、异常和边界测试。

## Copilot 实验步骤

先要求 Copilot 给出实施计划，不要立即修改文件；然后要求它只实现最小改动、展示 Diff 并运行测试。最后将生成的实现与验收标准逐条对照。
