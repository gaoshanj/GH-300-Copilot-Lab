# GH-300 Copilot 实验操作手册

本手册用于课堂现场操作。除特别说明外，所有命令都在仓库根目录执行。学员可以使用 GitHub Codespaces，也可以使用本地 VS Code。

## 0. 统一环境准备

### 0.1 打开实验环境

1. 打开 [GH-300-Copilot-Lab](https://github.com/gaoshanj/GH-300-Copilot-Lab)。
2. 选择 **Code → Codespaces → Create codespace on main**。
3. 等待 Codespace 初始化完成。`.devcontainer/devcontainer.json` 会自动安装 Python、Copilot 和 Python 扩展。
4. 在 VS Code 的 Chat 面板确认可以选择 **Ask** 和 **Agent**。
5. 打开仓库中的 `.github/copilot-instructions.md`，阅读项目约束。

### 0.2 启动项目并建立基线

在 VS Code Terminal 执行：

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
```

预期结果：`4 passed, 1 xfailed`。`xfailed` 是故意保留的 Bug 实验，不是环境故障。

启动 API：

```bash
uvicorn app.main:app --reload
```

在浏览器打开 `http://127.0.0.1:8000/docs`。Codespaces 环境请选择 **Open in Browser** 查看 Swagger UI。

### 0.3 课堂统一规则

- 先让 Copilot 解释计划，再允许它修改文件。
- 每次只处理一个明确目标。
- 接受建议前检查 Diff。
- 任何行为变化都要有测试。
- 不要将真实密钥、客户数据和生产日志粘贴到 Copilot。
- 只有看到实际测试输出，才能判断实验完成。

---

## Lab 01：从 Business Request 生成 API

**目标**：把结构化业务需求转换为最小可验证的代码变更。

**涉及能力**：Chat、Plan-first prompting、Inline Chat、pytest。

### 操作步骤

1. 打开 `docs/business-request.md`，阅读 Context 和 Acceptance criteria。
2. 在 Copilot Chat 选择 **Ask**，发送：

   ```text
   请阅读 docs/business-request.md、app/main.py 和 tests/test_api.py。
   先不要修改文件。请输出：
   1) 需求拆解；
   2) 需要新增或修改的文件；
   3) API 响应契约；
   4) 正常、异常和边界测试；
   5) 你不确定的假设。
   ```

3. 检查计划是否包含 `POST /checksum`、空文本、长度上限、确定性和测试。
4. 切换到 **Agent**，发送：

   ```text
   按刚才的计划实现最小改动。只处理 checksum 需求。
   先展示将要修改的文件，完成后运行与该需求相关的 pytest。
   不要修改无关的订单逻辑。
   ```

5. 审阅 Agent 的 Diff，确认 `TextRequest` 的校验边界没有被删除。
6. 手工验证接口：

   ```bash
   curl -X POST http://127.0.0.1:8000/checksum ^
     -H "Content-Type: application/json" ^
     -d "{\"text\":\"hello\"}"
   ```

   macOS/Linux 将 `^` 替换为 `\`。

### 预期结果

- 返回 HTTP 200。
- 响应包含整数 `checksum`。
- 相同的 `"hello"` 请求重复执行时结果一致。
- 空文本返回 HTTP 422。
- `pytest -q` 仍然通过，且没有修改订单相关代码。

### 完成标准

学员能够指出：业务需求如何变成代码、测试和可验证的 API 契约，而不是只展示 Copilot 生成了代码。

---

## Lab 02：使用 Agent mode 修复 Bug

**目标**：完成“复现 → 根因 → 回归测试 → 最小修复 → 全量验证”的调试闭环。

**涉及能力**：Agent mode、`/fix`、测试驱动排障。

### 操作步骤

1. 打开 `docs/bug-report.md`。
2. 确认缺陷：

   ```bash
   curl http://127.0.0.1:8000/orders/demo-100
   ```

   预期会看到 `total` 为 `15.5`，而正确结果应为 `28.0`。

3. 在 `app/service.py` 中选中 `summarize_order`，打开 Inline Chat，输入：

   ```text
   /explain 请解释 total 的计算逻辑，并指出它是否正确处理了 quantity。
   ```

4. 阅读解释后，不要马上接受修改。先在 Copilot Chat 发送：

   ```text
   根据 docs/bug-report.md，先提出一个能够稳定复现该缺陷的回归测试。
   说明测试为什么能证明 quantity 被正确计算。
   不要修改实现。
   ```

5. 让 Copilot 添加回归测试并运行聚焦测试：

   ```text
   请只添加回归测试，不修改 app/service.py。运行：
   python -m pytest tests/test_api.py::test_order_total_includes_quantity -q
   报告实际失败信息。
   ```

6. 确认测试失败后，在 `summarize_order` 上使用：

   ```text
   /fix 请修复 quantity 未计入 total 的问题。保持响应字段和四舍五入行为不变。
   ```

7. 检查 Diff，确认修复是 `quantity * price`，没有改动订单响应结构。
8. 执行完整验证：

   ```bash
   python -m pytest -q
   curl http://127.0.0.1:8000/orders/demo-100
   ```

### 预期结果

- `demo-100` 的 `total` 为 `28.0`。
- 回归测试由 xfail 变为正常通过，或在课堂上移除 xfail 后通过。
- 其他测试仍然通过。
- Copilot 能够说明根因，而不只是返回一段看似合理的代码。

### 完成标准

学员必须提交：根因说明、回归测试、最小 Diff 和测试输出四项证据。

---

## Lab 03：根据需求设计边界测试

**目标**：让 Copilot 从验收标准生成测试矩阵，而不是盲目生成大量测试。

**涉及能力**：Prompt File、测试矩阵、边界条件。

### 操作步骤

1. 打开 `.github/prompts/test-design.prompt.md`。
2. 在 Copilot Chat 中运行该 Prompt File，或复制以下提示词：

   ```text
   阅读 docs/business-request.md 和当前实现。
   请用表格设计测试矩阵，列出：
   - 正常输入；
   - 空字符串；
   - 1 个字符；
   - 10,000 个字符；
   - 10,001 个字符；
   - Unicode 文本；
   - 相同输入重复调用；
   - 缺少 text 字段。
   每行说明预期状态码、预期行为和测试优先级。
   ```

3. 检查 Copilot 是否区分“输入被拒绝”和“输入被接受但结果不同”。
4. 选择至少 5 个必须测试，让 Copilot 生成测试代码：

   ```text
   根据测试矩阵，只实现标记为 must-have 的测试。
   使用现有 pytest 风格，不修改生产实现。
   运行新增测试并报告覆盖的验收标准。
   ```

5. 审阅每个断言，确认它验证的是业务行为，而不是只验证 HTTP 200。
6. 执行：

   ```bash
   python -m pytest tests/test_api.py -q
   ```

### 预期结果

- 测试覆盖正常、非法、边界和确定性场景。
- 10,001 个字符被拒绝。
- 缺少 `text` 字段被拒绝。
- 不因为测试生成而修改 API 契约。

### 完成标准

学员能够解释每个测试对应的验收标准，并指出至少一个 Copilot 生成但需要人工加强的断言。

---

## Lab 04：分析测试日志并形成 Bug 报告

**目标**：从脱敏日志中提取事实、建立时间线和验证假设，不臆测日志没有提供的信息。

**涉及能力**：日志分析、Copilot Chat、Copilot CLI 思维方式。

### 操作步骤

1. 打开 `logs/api.log`，确认日志中没有真实客户数据。
2. 运行 Prompt File `.github/prompts/log-analysis.prompt.md`，或发送：

   ```text
   请只根据 logs/api.log 分析问题，不要编造日志中不存在的事实。
   按以下结构输出中文 Bug 报告：
   症状、影响、时间线、证据、最可能根因、复现命令、
   建议回归测试、仍需确认的问题。
   ```

3. 检查时间线是否正确关联了请求、警告和测试失败。
4. 追问：

   ```text
   请把“日志直接证明的事实”和“需要验证的假设”分成两栏。
   对每个假设给出一个最小验证动作。
   ```

5. 在 Terminal 中使用普通命令验证日志事实：

   ```bash
   findstr "ERROR WARN" logs/api.log
   ```

   macOS/Linux 使用：

   ```bash
   grep -E "ERROR|WARN" logs/api.log
   ```

6. 将 Copilot 输出与命令结果对照，修正报告中的臆测。

### 预期结果

报告至少应指出：`demo-100` 预期 `28.00`、实际 `15.50`，并且存在对应测试失败；不能声称已经证明数据库、网络或权限是根因。

### 完成标准

输出一份包含“事实 / 假设 / 验证动作”三部分的中文 Bug 报告。

---

## Lab 05：完成一次 Code Review

**目标**：以 Reviewer 身份发现正确性、安全性、回归风险和测试缺口。

**涉及能力**：Review Prompt、Diff 审阅、证据化反馈。

### 操作步骤

1. 先完成 Lab 02 的修复，使用以下命令查看变更：

   ```bash
   git diff
   ```

2. 在 Copilot Chat 中选择 `.github/agents/reviewer.agent.md` 对当前 Diff 执行 Review。
3. 如果没有 Git 提交，可让 Copilot Review 当前工作区 Diff：

   ```text
   只审阅当前 git diff，不修改文件。
   按 Correctness、Security、Regression、Tests 四个维度输出发现。
   每条发现必须包含严重性、文件/行号、影响、证据和建议验证动作。
   ```

4. 对每条 Review 建议执行人工验证：

   ```text
   请不要直接修改。针对这条发现，指出对应代码行、可复现输入和验证命令。
   ```

5. 检查 Review 是否遗漏：

   - 数量大于 1 时的金额计算；
   - 输入长度和空值；
   - 响应结构兼容性；
   - 是否存在足够的回归测试；
   - 是否引入密钥、日志泄露或危险命令。

6. 运行：

   ```bash
   python -m pytest -q
   git diff --check
   ```

### 预期结果

- Review 结论引用具体文件和代码，而不是泛泛说“看起来不错”。
- 已验证的问题与未验证的建议明确区分。
- 没有因为 Review 自动修改而产生未经检查的额外 Diff。

### 完成标准

提交一份包含至少 1 条有效发现和验证证据的 Review 记录。

---

## Lab 06：使用仓库指令、Prompt File 和自定义 Agent

**目标**：把个人 Copilot 技巧固化为可共享、可审阅、可版本控制的团队资产。

**涉及能力**：`copilot-instructions.md`、Prompt File、Custom Agent、长对话约束。

### 操作步骤

1. 阅读 `.github/copilot-instructions.md`，找出至少 3 条项目规则。
2. 新建或修改一个 Prompt File，要求它包含：

   - `description`；
   - 明确的输入文件；
   - 先计划后修改；
   - 测试命令；
   - 输出格式；
   - 失败时不得臆测。

3. 在新会话中运行该 Prompt File，观察仓库指令是否自动影响 Copilot 的回答。
4. 打开 `.github/agents/reviewer.agent.md`，确认它要求：

   - 只审阅 Diff；
   - 不修改文件；
   - 提供文件/行号；
   - 报告测试缺口；
   - 支持中文输出。

5. 让自定义 Agent Review 一个小范围 Diff：

   ```text
   请审阅当前 Diff。不要修改文件。中文输出，保留 Python 标识符和命令原文。
   只报告有证据支持的问题，并给出最小验证命令。
   ```

6. 开一个新的 Chat 会话，不重复粘贴全部规则，再询问：

   ```text
   根据仓库规则，如何判断本次修复可以提交？
   请列出必须运行的命令和必须检查的证据。
   ```

7. 检查回答是否遵守仓库规则；如果没有，更新指令文件并重新测试。

### 预期结果

- 团队成员可以复用相同 Prompt，而不需要重新描述整个流程。
- Agent 的职责、工具和权限边界清晰。
- 规则文件、Prompt File 和 Agent 都可以通过 Git Diff 审阅。

### 完成标准

学员提交一份团队 Copilot 资产清单，至少包含 1 个仓库指令、1 个 Prompt File、1 个 Agent，以及每个资产的适用场景和风险边界。

---

## Lab 07：将日志分析固化为可复用 Skill

**目标**：把一次性的日志分析 Prompt 变成团队可共享、可版本控制、可复用的 Skill。

**涉及能力**：Skills、结构化输出、证据和假设分离、日志脱敏。

### 操作步骤

1. 打开 `.github/skills/log-analysis-report/SKILL.md`，阅读目标、输入、步骤、输出格式和安全约束。
2. 在 Copilot Chat 中发送：

   ```text
   请使用 .github/skills/log-analysis-report/SKILL.md 分析 logs/api.log。
   只读取日志和 docs/bug-report.md，不修改任何文件。
   输出中文 Bug 报告，并明确区分事实证据、根因假设和未知信息。
   ```

3. 检查报告是否包含症状、影响、时间线、复现步骤、回归测试和下一步。
4. 追问：

   ```text
   请逐条标注你的结论来自哪一行日志。
   没有日志证据的内容改写为“需要验证的假设”。
   不要输出任何可能的密钥、Cookie、个人数据或完整请求体。
   ```

5. 将报告保存为临时文件或复制到 Issue 草稿中；不要覆盖原始 `logs/api.log`。
6. 修改一条 Skill 规则，例如增加“必须报告请求耗时”，再次运行并比较输出是否稳定。
7. 检查 Git Diff，确认只修改了 Skill 或报告草稿，没有把敏感日志提交到仓库。

### 预期结果

- 同一份日志在不同会话中遵循相同报告结构。
- 报告能区分事实、推断和未知信息。
- Skill 可以被其他成员或 Agent 复用，而不需要重新粘贴完整操作规范。

### 完成标准

学员提交一份结构化 Bug 报告，并能说明 Skill 中哪条规则防止了臆测或敏感信息泄露。

---

## Lab 08：优化 Token 成本并比较前后差异

**目标**：通过压缩上下文、缓存稳定规则和复用 Skill，减少重复输入；同时保留验收标准和关键证据。

**重要说明**：本实验使用透明的估算脚本，不代表 GitHub Copilot 的实际账单。实际消耗和价格取决于产品、模型、账户策略、输入/输出 Token 以及缓存规则。

**涉及能力**：Context engineering、context caching、context compression、Skills、成本度量。

### 操作步骤

1. 先运行基线估算：

   ```bash
   python tools/token_cost_demo.py
   ```

2. 记录输出中的：

   - `Baseline input tokens`
   - `Optimized input tokens`
   - `Tokens saved`
   - `Baseline cost proxy`
   - `Optimized cost proxy`
   - `With cached context`

3. 观察脚本中的基线上下文。它把 README、业务需求、Bug 报告、完整实验手册、日志和仓库指令全部拼接到一次请求中，模拟“把所有内容都贴给 Copilot”的低效方式。
4. 打开 `.github/skills/context-optimizer/SKILL.md`，用以下提示词让 Copilot 设计压缩方案：

   ```text
   请使用 .github/skills/context-optimizer/SKILL.md。
   比较 tools/token_cost_demo.py 中的 baseline 和 optimized 上下文。
   说明哪些内容被删除、压缩或移入 Skill，哪些验收标准和证据必须保留。
   不要修改文件，先输出 Context 优化报告。
   ```

5. 对比两种上下文的组成：

   | 方式 | 上下文内容 | 适用场景 |
   |---|---|---|
   | Baseline | 所有背景文档、完整手册、完整日志和规则 | 初次探索，但重复内容多 |
   | Compressed | 任务 Skill、相关 Bug 报告、必要日志和输出格式 | 已明确目标的任务 |
   | Cached | 稳定规则放入 Skill，重复请求只传变化部分 | 团队长期复用 |

6. 修改 `tools/token_cost_demo.py` 的 `load_optimized`，只保留完成 Lab 07 所需的最小证据，再运行脚本。
7. 使用不同价格参数做敏感性分析：

   ```bash
   python tools/token_cost_demo.py --input-rate 0.00001
   python tools/token_cost_demo.py --input-rate 0.00001 --cached-discount 0.95
   ```

8. 验证优化没有损失任务目标：

   ```text
   使用优化后的上下文生成日志报告。
   必须仍然输出：事实证据、时间线、根因假设、复现步骤、回归测试和下一步。
   将结果与 Lab 07 的报告逐项比较，不要只比较字数。
   ```

9. 记录一张前后对比表：

   | 指标 | 优化前 | 优化后 | 结论 |
   |---|---:|---:|---|
   | 估算输入 Token | 运行脚本填写 | 运行脚本填写 | 是否减少 |
   | 成本代理值 | 运行脚本填写 | 运行脚本填写 | 是否降低 |
   | 必需证据是否完整 | 是/否 | 是/否 | 是否可接受 |
   | 报告结构是否稳定 | 是/否 | 是/否 | 是否可复用 |

### 预期结果

- 优化后的估算输入 Token 少于基线。
- 使用 Skill 后，重复的操作规范不需要每轮重新粘贴。
- 缓存适合稳定、不含敏感信息的规则和格式，不应缓存一次性的客户数据或生产日志。
- 优化后仍保留业务目标、验收标准、错误证据和安全约束。

### 完成标准

学员提交前后成本对比表，并明确写出：

1. 哪些内容被压缩或移入 Skill；
2. 哪些内容不能删除；
3. 估算值与真实 Copilot 消耗的差异；
4. 优化后如何证明输出质量没有下降。

---

## 综合验收

完成 8 个实验后，学员应能走通以下闭环：

```text
业务需求
  → 结构化 Prompt
  → 小步实现
  → 测试设计
  → Bug 复现与修复
  → 日志分析
  → Code Review
  → 可复用的日志报告 Skill
  → 上下文压缩与成本度量
  → 可共享的团队规则
```

最终执行：

```bash
python -m pytest -q
git diff --check
```

提交前确认：代码、测试、日志分析和 Review 结论均有可复现证据；任何 Copilot 建议都经过人工检查。
