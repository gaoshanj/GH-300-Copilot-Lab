# GH-300 Copilot Applied Lab

This public lab is a companion repository for a customized GH-300 workshop. It is designed for GitHub Codespaces and VS Code with GitHub Copilot enabled.

## Learning path

| Lab | Scenario | Expected outcome |
|---|---|---|
| 01 | Business request to code | Turn a structured request into a small FastAPI change |
| 02 | Bug diagnosis | Use Agent mode and `/fix` to reproduce, explain, and repair a defect |
| 03 | Test design | Generate boundary-focused tests and verify them with `pytest` |
| 04 | Log analysis | Use Copilot Chat/CLI to correlate logs and write a concise bug report |
| 05 | Code review | Review a change for correctness, security, and missing tests |
| 06 | Team customization | Apply repository instructions, prompt files, and a custom agent |

The labs intentionally contain small, safe defects. Do not copy generated code directly to production: inspect the diff, run the tests, and make the final decision yourself.

## Start

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API.

## Copilot setup

1. Open this repository in GitHub Codespaces or VS Code.
2. Sign in to GitHub and verify that Copilot Chat and Agent mode are available.
3. Read `.github/copilot-instructions.md`.
4. Use the prompt files under `.github/prompts/` as repeatable exercises.
5. Treat tool calls, file edits, and test results as reviewable changes.

## Safety and privacy

- Never place credentials, customer data, production logs, or personal data in prompts.
- Review the repository's Copilot policy and content-exclusion settings before using similar patterns in a real organization.
- The examples are educational and do not provide legal advice about copyright, licensing, or IP indemnity.

## Suggested capstone

Start from `docs/business-request.md`, implement the endpoint, add tests, reproduce the defect in `docs/bug-report.md`, analyze `logs/api.log`, and open a pull request. Ask Copilot to review the PR and compare its findings with your own checklist.

