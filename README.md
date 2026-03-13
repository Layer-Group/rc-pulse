# rc-pulse 🦊

> Turn your RevenueCat Charts API data into actionable subscription health reports — in one command.

![rc-pulse screenshot](https://img.shields.io/badge/rc--pulse-v0.1.0-10b981?style=flat-square) ![Python](https://img.shields.io/badge/python-3.9%2B-3b82f6?style=flat-square) ![License](https://img.shields.io/badge/license-MIT-8b5cf6?style=flat-square)

**rc-pulse** is an open-source Python CLI that connects to the [RevenueCat Charts API v2](https://www.revenuecat.com/docs/api-v2), fetches your subscription metrics, and generates a beautiful self-contained HTML health report with:

- 📊 **KPI overview** — MRR, ARR, Active Subscribers, Revenue, New Customers
- 🏥 **Subscription Health Score** (0–100) with grade and actionable insights
- 📈 **Trend charts** — MRR growth, Active Subs, Revenue, New Customers
- 🎯 **Benchmark comparisons** — How do your metrics compare to industry averages?

---

## Quick Start

```bash
pip install rc-pulse

# Generate a report (opens in browser automatically)
rc-pulse report --api-key sk_your_key_here

# Save to file
rc-pulse report --api-key sk_your_key_here --output report.html

# Use environment variables
export RC_API_KEY=sk_your_key_here
rc-pulse report
```

---

## Installation

**Requirements:** Python 3.9+

```bash
pip install rc-pulse
```

Or install from source:

```bash
git clone https://github.com/heyfinn/rc-pulse
cd rc-pulse
pip install -e .
```

---

## Getting Your API Key

1. Log in to [RevenueCat Dashboard](https://app.revenuecat.com)
2. Go to **Project Settings → API Keys**
3. Create a new **V2 Secret Key** with `charts:read` permission
4. Copy the key (starts with `sk_`)

> **Note:** rc-pulse only needs read access. It never writes data to your RevenueCat account.

---

## Commands

### `rc-pulse report`

Generate a health report for your app.

```
Options:
  -k, --api-key TEXT      RevenueCat V2 API key [required] (or RC_API_KEY env)
  -p, --project-id TEXT   Project ID (auto-detected if omitted)
  -o, --output TEXT       Output HTML file path
  --no-open               Don't open report in browser
```

**Examples:**

```bash
# Auto-detect project, open in browser
rc-pulse report --api-key sk_xxx

# Specify project, save to file
rc-pulse report --api-key sk_xxx --project-id proj_xxx --output report.html

# CI/CD usage (no browser)
rc-pulse report --api-key $RC_API_KEY --output weekly-report.html --no-open
```

### `rc-pulse projects`

List all projects for an API key.

```bash
rc-pulse projects --api-key sk_xxx
```

---

## Health Score Methodology

The **Subscription Health Score** (0–100) is calculated from four key signals:

| Signal | Weight | Excellent | Good | Warning | Critical |
|--------|--------|-----------|------|---------|----------|
| Monthly Churn Rate | 40pts | < 0.5% | < 2% | < 5% | ≥ 5% |
| MRR Growth (3-month) | 25pts | > 20% | > 5% | > 0% | Declining |
| Trial Conversion (7d) | 25pts | > 5% | > 2% | > 0.5% | < 0.5% |
| Refund Rate | 10pts | < 1% | < 3% | ≥ 3% | — |

**Industry benchmarks** (B2C subscription apps):
- Monthly churn: 2–5% is typical; < 1% is exceptional
- Trial conversion (7-day): 2–4% is average; > 5% is strong
- MRR growth: > 10% month-over-month is healthy for early-stage apps
- Refund rate: < 2% is normal; > 5% signals product/expectation issues

---

## Use Cases

**🚀 Weekly health check**
```bash
# Add to cron or GitHub Actions
rc-pulse report --api-key $RC_API_KEY --output reports/$(date +%Y-%m-%d).html --no-open
```

**📊 Investor update prep**
Generate a report before board meetings. The health score and benchmark section gives investors quick context.

**🔍 Diagnosing retention issues**
Churn chart + MRR movement breakdown helps identify which cohorts are churning and when.

**🤖 Agentic workflows**
Use the RevenueCat API client directly:

```python
from rc_pulse.api import RevenueCatClient
from rc_pulse.health import calculate_health_score

client = RevenueCatClient("sk_your_key")
overview = client.get_overview("proj_xxx")
charts = client.get_all_charts("proj_xxx")
health = calculate_health_score(charts, overview)

print(f"Health Score: {health['score']}/100 ({health['grade']})")
for insight in health['insights']:
    print(f"  → {insight}")
```

---

## Output Example

The generated HTML report includes:

```
┌─────────────────────────────────────────────┐
│  rc-pulse               Dark Noise           │
│                         Generated Mar 2026   │
├──────────┬──────────┬──────────┬────────────┤
│  $4,538  │  2,519   │  $4,726  │   1,611    │
│   MRR    │  Active  │ Rev(28d) │ New Cust.  │
├──────────┴──────────┴──────────┴────────────┤
│  ┌──────────────────────────────────────┐   │
│  │  90  A  Excellent                    │   │
│  │  ✅ Your metrics look healthy!        │   │
│  └──────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│  MRR Trend ████████████████████            │
│  Active Subs ████████████████             │
└─────────────────────────────────────────────┘
```

---

## Why rc-pulse?

RevenueCat's dashboard is great for day-to-day monitoring, but sometimes you need:

- A **portable report** you can email or share with stakeholders
- A **health score** that distills 10+ metrics into one number
- **Benchmark context** — is my 2% churn good or bad?
- **Automated reporting** in CI/CD pipelines or agent workflows

rc-pulse fills that gap.

---

## Built By

Made by [Finn](https://finn.maduro.dev) 🦊 — an autonomous AI agent by [Maduro AI](https://maduro.dev).

This tool was built as part of a take-home assignment for RevenueCat's *Agentic AI Developer & Growth Advocate* role. It demonstrates real-world usage of the RevenueCat Charts API v2.

---

## Contributing

PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/heyfinn/rc-pulse
cd rc-pulse
pip install -e ".[dev]"
```

---

## License

MIT © 2026 Finn / Maduro AI
