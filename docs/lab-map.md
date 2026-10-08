# 客户需求与实验映射 Customer scenario map

| 客户需求 | 实验 | Copilot 能力 | 交付证据 |
|---|---:|---|---|
| Bug / debug | 02 | Agent mode, `/fix`, focused tests | regression test + diff |
| Test design and automation | 03 | Chat, prompt file, test matrix | pytest output |
| Test log and error analysis | 04 | Chat/CLI, structured reasoning | sanitized bug report |
| Business request to code | 01 | plan-first prompting, multi-file edit | acceptance criteria |
| Keep constraints across dialogue | 06 | instructions, prompt files, custom agent | versioned configuration |
| Code review | 05 | IDE/PR review workflow | findings with file/line evidence |
| Security, IP, privacy | all | responsible-use checklist, content boundaries | review checklist |
