# rc-pulse 🦊

> Turn your RevenueCat Charts API data into actionable subscription health reports — in one command, or directly in the browser.

[![rc-pulse](https://img.shields.io/badge/rc--pulse-v0.2.0-10b981?style=flat-square)](https://layer-group.github.io/rc-pulse/)
[![Python](https://img.shields.io/badge/python-3.9%2B-3b82f6?style=flat-square)](https://pypi.org/project/rc-pulse/)
[![License](https://img.shields.io/badge/license-MIT-8b5cf6?style=flat-square)](LICENSE)
[![Built by AI](https://img.shields.io/badge/built%20by-Finn%20%F0%9F%A6%8A%20AI%20Agent-f59e0b?style=flat-square)](https://finn.maduro.dev)

---

## 🌐 [Live Web Dashboard →](https://layer-group.github.io/rc-pulse/)

**No install needed.** Open the dashboard, paste your RevenueCat API key (or click "Demo Mode" to see real Dark Noise data), and get instant charts, health score, and benchmarks — all 100% client-side.

---

## What rc-pulse gives you

| Feature | Web Dashboard | Python CLI |
|---------|:---:|:---:|
| KPI overview (MRR, ARR, Active Subs, Revenue) | ✅ | ✅ |
| Subscription Health Score (0–100 with grade) | ✅ | ✅ |
| Industry benchmark comparisons | ✅ | ✅ |
| MRR trend chart | ✅ | ✅ |
| Active subscriptions chart | ✅ | ✅ |
| Revenue chart | ✅ | ✅ |
| MRR growth momentum chart | ✅ | ✅ |
| Actionable insights | ✅ | ✅ |
| Demo mode (real Dark Noise data) | ✅ | ❌ |
| Saveable HTML report | ❌ | ✅ |
| CI/CD / automation | ❌ | ✅ |
| Zero data stored | ✅ (browser) | ✅ (local) |

---

## 🚀 Web Dashboard Quick Start

1. Go to **[layer-group.github.io/rc-pulse](https://layer-group.github.io/rc-pulse/)**
2. Enter your RevenueCat V2 API key (needs `charts:read` scope)
3. Click **Analyze →**

Your key never leaves your browser. Requests go directly to the RevenueCat API via CORS.

**Don't have a key?** Click "View Dark Noise demo" to explore with real data.

---

## 🐍 Python CLI Quick Start

```bash
pip install rc-pulse

# Generate a report (opens in browser)
rc-pulse report --api-key sk_your_key_here

# Save to file
rc-pulse report --api-key sk_your_key_here --output report.html

# Use environment variable
export RC_API_KEY=sk_your_key_here
rc-pulse report
```

**Or install from source:**

```bash
git clone https://github.com/Layer-Group/rc-pulse
cd rc-pulse
pip install -e .
```

---

## Getting Your API Key

1. Log in to [RevenueCat Dashboard](https://app.revenuecat.com)
2. Go to **Project Settings → API Keys**
3. Create a new **V2 Secret Key** with `charts:read` permission
4. Copy the key (starts with `sk_`)

> **Security note:** rc-pulse only needs read access. It never writes data to your RevenueCat account. In the web dashboard, your key is never stored — it lives only in your browser session.

---

## Python CLI Commands

### `rc-pulse report`

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

```bash
rc-pulse projects --api-key sk_xxx
```

---

## Health Score Methodology

The **Subscription Health Score** (0–100) is calculated from three key signals:

| Signal | Weight | Excellent | Good | Warning | Critical |
|--------|--------|-----------|------|---------|----------|
| Monthly Churn Rate | 40pts | < 0.5% | < 2% | < 2–5% | ≥ 5% |
| MRR Growth (3-month) | 35pts | > 20% | > 5% | 0–5% | Declining |
| Refund Rate | 15pts | < 1% | < 3% | ≥ 3% | — |

**Industry benchmarks** (B2C subscription apps):
- Monthly churn: 2–5% is typical; < 1% is exceptional
- MRR growth: > 10% month-over-month is healthy for early-stage apps
- Refund rate: < 2% is normal; > 5% signals product/expectation issues

---

## Use Cases

**🚀 Weekly health check (CLI)**
```bash
# Add to cron or GitHub Actions
rc-pulse report --api-key $RC_API_KEY --output reports/$(date +%Y-%m-%d).html --no-open
```

**📊 Investor update prep**
Generate a report before board meetings. The health score and benchmark section gives investors quick context.

**🔍 Diagnosing retention issues**
The churn chart + MRR growth breakdown helps identify cohort-level retention patterns.

**🤖 Agentic workflows (Python library)**
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

**🔗 Quick share (Web Dashboard)**
Share the [live dashboard link](https://layer-group.github.io/rc-pulse/) with your team and have everyone use their own key.

---

## Architecture

```
rc-pulse web dashboard
┌─────────────────────────────────────────────────────┐
│  Browser (client-side only)                         │
│                                                     │
│  index.html  →  fetch('api.revenuecat.com/v2/...')  │
│                         ↓                           │
│              Parse + calculate health score         │
│                         ↓                           │
│              Render Chart.js charts                 │
│                                                     │
│  ✅ No server, no proxy, no data storage           │
└─────────────────────────────────────────────────────┘

rc-pulse Python CLI
┌─────────────────────────────────────────────────────┐
│  rc_pulse/api.py   →  RevenueCat API v2             │
│  rc_pulse/health.py →  Score calculation            │
│  rc_pulse/report.py →  HTML report generation       │
│  rc_pulse/cli.py   →  Click CLI entrypoint          │
└─────────────────────────────────────────────────────┘
```

---

## Built By

Made by [Finn](https://finn.maduro.dev) 🦊 — an autonomous AI agent by [Maduro AI](https://maduro.dev).

> 🤖 **Full disclosure:** Finn is an AI agent, not a human developer. This tool was built as part of a take-home assignment for RevenueCat's *Agentic AI Developer & Growth Advocate* role. The data used in demo mode belongs to Dark Noise (a real app by Charlie Chapman) — used with the provided read-only API key.

---

## Contributing

PRs welcome!

```bash
git clone https://github.com/Layer-Group/rc-pulse
cd rc-pulse
pip install -e ".[dev]"
```

---

## License

MIT © 2026 Finn / Maduro AI
