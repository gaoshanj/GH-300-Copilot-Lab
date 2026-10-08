# GH-300 Copilot 实战实验 Lab

这是定制版 GH-300 课程的配套公开实验仓库，面向已启用 GitHub Copilot 的 GitHub Codespaces 和 VS Code 环境。仓库中的英文名称、命令、API 路径和配置键保持原样，便于学员在真实开发工具中操作。

## 实验路线

完整的中文逐步操作手册见 [`docs/lab-manual.md`](docs/lab-manual.md)。课堂讲师可以按 Lab 01 到 Lab 06 顺序授课，学员可以逐项对照“预期结果”和“完成标准”自检。

| Lab | Scenario | Expected outcome |
|---|---|---|
| 01 | Business request to code / 从业务需求到代码 | 将结构化业务需求转换为一个小型 FastAPI 改动 |
| 02 | Bug diagnosis / Bug 定位 | 使用 Agent mode 和 `/fix` 复现、解释并修复缺陷 |
| 03 | Test design / 测试设计 | 生成边界测试，并用 `pytest` 验证 |
| 04 | Log analysis / 日志分析 | 使用 Copilot Chat/CLI 关联日志并形成 Bug 报告 |
| 05 | Code review / 代码评审 | 检查正确性、安全性和测试缺口 |
| 06 | Team customization / 团队定制 | 应用仓库指令、Prompt File 和自定义 Agent |
| 07 | Reusable log-report Skill / 可复用日志报告 Skill | 将测试日志稳定转换为有证据的中文 Bug 报告 |
| 08 | Token optimization / Token 成本优化 | 对比完整上下文、压缩上下文、缓存和 Skill 化后的成本代理值 |

实验中故意保留了小型且安全的缺陷，用于练习排障闭环。不要直接把 Copilot 生成的代码用于生产环境：必须检查 Diff、运行测试，并由开发者做最终决定。

## 开始实验

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API.

打开 `http://127.0.0.1:8000/docs`，可以通过 Swagger UI 调用示例 API。

## Copilot 环境准备

1. 在 GitHub Codespaces 或 VS Code 中打开本仓库。
2. 登录 GitHub，确认 Copilot Chat 和 Agent mode 可用。
3. 阅读 `.github/copilot-instructions.md`，理解本项目的质量和安全要求。
4. 使用 `.github/prompts/` 下的 Prompt File 重复练习。
5. 把工具调用、文件修改和测试结果都当作需要审阅的变更。

## 安全与隐私

- 不要把凭据、客户数据、生产日志或个人数据放入 Prompt。
- 在真实组织中复用类似做法前，先检查组织的 Copilot Policy 和 Content Exclusion 设置。
- 本仓库仅用于教学，不构成关于版权、许可证或 IP Indemnity 的法律建议。

## 综合实战建议

从 `docs/business-request.md` 开始，实现接口并补充测试；然后按照 `docs/bug-report.md` 复现缺陷，分析 `logs/api.log`，最后创建 Pull Request。让 Copilot Review 该 PR，并将它的发现与你的人工检查清单进行对比。
