"""HTML report generator for rc-pulse."""
import json
from datetime import datetime, timezone


TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>rc-pulse | {{ app_name }} Health Report</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg: #0f172a; --surface: #1e293b; --surface2: #273449;
      --border: #334155; --text: #f1f5f9; --muted: #94a3b8;
      --green: #10b981; --blue: #3b82f6; --yellow: #f59e0b;
      --red: #ef4444; --purple: #8b5cf6;
    }
    body { background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, sans-serif; min-height: 100vh; }
    .container { max-width: 1100px; margin: 0 auto; padding: 2rem 1.5rem; }
    header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border); }
    .logo { font-size: 1.5rem; font-weight: 800; color: var(--text); }
    .logo span { color: var(--green); }
    .meta { color: var(--muted); font-size: 0.875rem; text-align: right; }
    .meta strong { color: var(--text); display: block; font-size: 1rem; }
    .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
    .kpi { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.25rem 1.5rem; }
    .kpi-label { color: var(--muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
    .kpi-value { font-size: 2rem; font-weight: 700; color: var(--text); }
    .kpi-sub { color: var(--muted); font-size: 0.8rem; margin-top: 0.25rem; }
    .section { margin-bottom: 2rem; }
    .section-title { font-size: 1.1rem; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1rem; }
    .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
    .chart-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; }
    .chart-title { font-size: 0.95rem; font-weight: 600; margin-bottom: 1rem; color: var(--text); }
    .chart-wrap { position: relative; height: 220px; }
    .health-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; display: grid; grid-template-columns: auto 1fr; gap: 2rem; align-items: start; margin-bottom: 2rem; }
    .health-score-circle { width: 120px; height: 120px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 4px solid; flex-shrink: 0; }
    .health-score-num { font-size: 2.2rem; font-weight: 800; line-height: 1; }
    .health-score-grade { font-size: 0.8rem; font-weight: 600; color: var(--muted); margin-top: 0.2rem; }
    .health-label { font-size: 1.1rem; font-weight: 700; margin-bottom: 0.75rem; }
    .insights { list-style: none; display: flex; flex-direction: column; gap: 0.5rem; }
    .insights li { font-size: 0.9rem; color: var(--muted); padding: 0.6rem 1rem; background: var(--surface2); border-radius: 8px; border-left: 3px solid var(--border); }
    .benchmarks { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }
    .benchmark { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 1rem 1.25rem; display: flex; flex-direction: column; gap: 0.3rem; }
    .benchmark-metric { font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }
    .benchmark-value { font-size: 1.4rem; font-weight: 700; }
    .benchmark-note { font-size: 0.75rem; color: var(--muted); }
    .status-excellent { color: var(--green); }
    .status-good { color: var(--blue); }
    .status-warning { color: var(--yellow); }
    .status-critical { color: var(--red); }
    footer { margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.8rem; display: flex; justify-content: space-between; }
    footer a { color: var(--green); text-decoration: none; }
    @media (max-width: 600px) {
      .charts-grid { grid-template-columns: 1fr; }
      .health-card { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
<div class="container">
  <header>
    <div class="logo">rc<span>-pulse</span></div>
    <div class="meta">
      <strong>{{ app_name }}</strong>
      Generated {{ generated_at }}
    </div>
  </header>

  <!-- KPI Overview -->
  <div class="section">
    <div class="section-title">Overview</div>
    <div class="kpi-grid">
      {{ kpi_cards }}
    </div>
  </div>

  <!-- Health Score -->
  <div class="section">
    <div class="section-title">Subscription Health</div>
    <div class="health-card">
      <div class="health-score-circle" style="border-color: {{ health_color }}; color: {{ health_color }};">
        <div class="health-score-num">{{ health_score }}</div>
        <div class="health-score-grade">{{ health_grade }}</div>
      </div>
      <div>
        <div class="health-label" style="color: {{ health_color }};">{{ health_label }}</div>
        <ul class="insights">
          {{ insight_items }}
        </ul>
      </div>
    </div>
  </div>

  <!-- Benchmarks -->
  {% if benchmarks %}
  <div class="section">
    <div class="section-title">Benchmarks</div>
    <div class="benchmarks">
      {{ benchmark_cards }}
    </div>
  </div>
  {% endif %}

  <!-- Charts -->
  <div class="section">
    <div class="section-title">Trends</div>
    <div class="charts-grid">
      <div class="chart-card">
        <div class="chart-title">📈 Monthly Recurring Revenue (MRR)</div>
        <div class="chart-wrap"><canvas id="mrrChart"></canvas></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">👥 Active Subscriptions</div>
        <div class="chart-wrap"><canvas id="activesChart"></canvas></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">💸 Revenue</div>
        <div class="chart-wrap"><canvas id="revenueChart"></canvas></div>
      </div>
      <div class="chart-card">
        <div class="chart-title">🆕 New Customers</div>
        <div class="chart-wrap"><canvas id="customersChart"></canvas></div>
      </div>
    </div>
  </div>

  <footer>
    <span>Generated by <a href="https://github.com/heyfinn/rc-pulse">rc-pulse</a> — open source RevenueCat health reporter</span>
    <span>Data from RevenueCat Charts API v2</span>
  </footer>
</div>

<script>
const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false }, tooltip: { backgroundColor: '#1e293b', borderColor: '#334155', borderWidth: 1, titleColor: '#f1f5f9', bodyColor: '#94a3b8' } },
  scales: {
    x: { grid: { color: '#1e293b' }, ticks: { color: '#64748b', maxTicksLimit: 8, font: { size: 11 } } },
    y: { grid: { color: '#1e293b' }, ticks: { color: '#64748b', font: { size: 11 } } }
  }
};

function makeChart(id, labels, data, color, prefix='') {
  const ctx = document.getElementById(id);
  if (!ctx) return;
  new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        data,
        borderColor: color,
        backgroundColor: color + '18',
        borderWidth: 2.5,
        fill: true,
        tension: 0.4,
        pointRadius: 3,
        pointHoverRadius: 5,
      }]
    },
    options: {
      ...chartDefaults,
      scales: {
        ...chartDefaults.scales,
        y: { ...chartDefaults.scales.y, ticks: { ...chartDefaults.scales.y.ticks, callback: v => prefix + v.toLocaleString() } }
      }
    }
  });
}

{{ chart_data_js }}
</script>
</body>
</html>"""


def _fmt_money(v):
    if v >= 1000:
        return f"${v/1000:.1f}k"
    return f"${v:.0f}"


def _fmt_num(v):
    if v >= 1000:
        return f"{v/1000:.1f}k"
    return f"{v:.0f}"


def _chart_values(chart_data, measure_idx=0):
    if not chart_data or not chart_data.get("values"):
        return [], []
    vals = [v for v in chart_data["values"] if not v.get("incomplete")]
    labels = [datetime.fromtimestamp(v["cohort"], tz=timezone.utc).strftime("%b %Y") for v in vals]
    values = [v["value"] for v in vals]
    return labels, values


def generate_report(app_name: str, overview: dict, charts: dict, health: dict) -> str:
    # KPI cards
    metrics = {m["id"]: m for m in overview.get("metrics", [])}
    kpi_cards = ""
    for mid, label, fmt in [
        ("mrr", "MRR", lambda v: f"${v:,.0f}"),
        ("active_subscriptions", "Active Subs", lambda v: f"{v:,}"),
        ("revenue", "Revenue (28d)", lambda v: f"${v:,.0f}"),
        ("new_customers", "New Customers (28d)", lambda v: f"{v:,}"),
        ("active_users", "Active Users (28d)", lambda v: f"{v:,}"),
        ("active_trials", "Active Trials", lambda v: f"{v:,}"),
    ]:
        if mid in metrics:
            m = metrics[mid]
            kpi_cards += f"""<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{fmt(m['value'])}</div></div>\n"""

    # Health score
    insight_items = "\n".join(f"<li>{i}</li>" for i in health["insights"])

    # Benchmarks
    benchmark_cards = ""
    for b in health.get("benchmarks", []):
        benchmark_cards += f"""<div class="benchmark">
  <div class="benchmark-metric">{b['metric']}</div>
  <div class="benchmark-value status-{b['status']}">{b['value']}</div>
  <div class="benchmark-note">{b['note']}</div>
</div>\n"""

    # Chart data JS
    mrr_labels, mrr_vals = _chart_values(charts.get("mrr"))
    actives_labels, actives_vals = _chart_values(charts.get("actives"))
    revenue_labels, revenue_vals = _chart_values(charts.get("revenue"))
    customers_labels, customers_vals = _chart_values(charts.get("customers_new"))

    chart_js = f"""
makeChart('mrrChart', {json.dumps(mrr_labels)}, {json.dumps(mrr_vals)}, '#10b981', '$');
makeChart('activesChart', {json.dumps(actives_labels)}, {json.dumps(actives_vals)}, '#3b82f6');
makeChart('revenueChart', {json.dumps(revenue_labels)}, {json.dumps(revenue_vals)}, '#8b5cf6', '$');
makeChart('customersChart', {json.dumps(customers_labels)}, {json.dumps(customers_vals)}, '#f59e0b');
"""

    has_benchmarks = bool(health.get("benchmarks"))

    html = TEMPLATE.replace("{{ app_name }}", app_name)
    html = html.replace("{{ generated_at }}", datetime.now().strftime("%B %d, %Y %H:%M UTC"))
    html = html.replace("{{ kpi_cards }}", kpi_cards)
    html = html.replace("{{ health_score }}", str(health["score"]))
    html = html.replace("{{ health_grade }}", health["grade"])
    html = html.replace("{{ health_label }}", health["label"])
    html = html.replace("{{ health_color }}", health["color"])
    html = html.replace("{{ insight_items }}", insight_items)
    html = html.replace("{{ benchmark_cards }}", benchmark_cards)
    html = html.replace("{{ chart_data_js }}", chart_js)
    html = html.replace("{% if benchmarks %}", "" if has_benchmarks else "<!--")
    html = html.replace("{% endif %}", "" if has_benchmarks else "-->")

    return html
