"""Compare baseline and optimized context using a transparent token-cost proxy.

This is an educational estimate, not a GitHub Copilot invoice calculator.
"""

from __future__ import annotations

import argparse
from pathlib import Path


def estimate_tokens(text: str) -> int:
    """Conservative rough estimate for mixed English/Chinese teaching text."""
    return max(1, (len(text) + 3) // 4)


def load_baseline(root: Path) -> str:
    paths = [
        root / "README.md",
        root / "docs" / "business-request.md",
        root / "docs" / "bug-report.md",
        root / "docs" / "lab-manual.md",
        root / "logs" / "api.log",
        root / ".github" / "copilot-instructions.md",
    ]
    return "\n\n".join(path.read_text(encoding="utf-8") for path in paths)


def load_optimized(root: Path) -> str:
    return "\n".join(
        [
            (root / ".github" / "skills" / "log-analysis-report" / "SKILL.md").read_text(
                encoding="utf-8"
            ),
            (root / "docs" / "bug-report.md").read_text(encoding="utf-8"),
            (root / "logs" / "api.log").read_text(encoding="utf-8"),
            "输出：事实、时间线、根因假设、复现步骤、回归测试和下一步。",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="估算 Copilot 上下文优化前后的成本代理值")
    parser.add_argument("--input-rate", type=float, default=0.000005)
    parser.add_argument("--cached-discount", type=float, default=0.9)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    baseline_tokens = estimate_tokens(load_baseline(root))
    optimized_tokens = estimate_tokens(load_optimized(root))
    saved = baseline_tokens - optimized_tokens
    reduction = saved / baseline_tokens if baseline_tokens else 0
    baseline_cost = baseline_tokens * args.input_rate
    optimized_cost = optimized_tokens * args.input_rate
    cached_cost = optimized_cost * (1 - args.cached_discount)

    print("Token Context Optimization (educational estimate)")
    print(f"Baseline input tokens : {baseline_tokens:,}")
    print(f"Optimized input tokens: {optimized_tokens:,}")
    print(f"Tokens saved          : {saved:,} ({reduction:.1%})")
    print(f"Baseline cost proxy   : ${baseline_cost:.6f}")
    print(f"Optimized cost proxy  : ${optimized_cost:.6f}")
    print(f"With cached context   : ${cached_cost:.6f}")
    print()
    print("说明：这是按字符长度估算的教学代理值，不是 GitHub Copilot 实际账单。")
    print("真实成本取决于 Copilot 产品、模型、账户策略、输入/输出 Token 和缓存规则。")


if __name__ == "__main__":
    main()

