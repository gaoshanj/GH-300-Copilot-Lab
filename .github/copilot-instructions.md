# GH-300 lab instructions

- Explain the plan before editing files.
- Treat `docs/business-request.md` as the acceptance criteria for the checksum exercise.
- Preserve the public API response shape unless the task explicitly requests a breaking change.
- Prefer small, typed Python functions and explicit error handling.
- For every behavior change, add or update a focused pytest test before declaring success.
- Do not claim tests pass unless you ran `pytest -q` and inspected the result.
- Never invent credentials, customer data, logs, or external API responses.
- For security-sensitive suggestions, identify the threat, the assumption, and the verification step.

