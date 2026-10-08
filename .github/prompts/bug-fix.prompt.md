---
mode: agent
description: Diagnose and repair one reproducible defect with a regression test. 诊断并修复一个可复现缺陷，同时增加回归测试。
---

阅读 `docs/bug-report.md`、相关实现和现有测试。
先解释可能的根因并提出回归测试，不要立即编辑文件。
获得确认后，实现最小修复，先运行聚焦测试，再运行完整测试套件。
报告变更文件、验证证据以及剩余的不确定性。
