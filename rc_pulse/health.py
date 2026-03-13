"""Subscription health score calculator."""


def calculate_health_score(charts: dict, overview: dict) -> dict:
    score = 100
    insights = []
    benchmarks = []

    # --- Churn Rate ---
    churn_data = charts.get("churn", {})
    churn_rate = None
    if churn_data and churn_data.get("summary"):
        churn_rate = churn_data["summary"].get("average", {}).get("Churn Rate")

    if churn_rate is not None:
        if churn_rate < 0.5:
            benchmarks.append({"metric": "Monthly Churn", "value": f"{churn_rate:.2f}%", "status": "excellent", "note": "Industry avg ~2.5%"})
        elif churn_rate < 2.0:
            score -= 10
            benchmarks.append({"metric": "Monthly Churn", "value": f"{churn_rate:.2f}%", "status": "good", "note": "Industry avg ~2.5%"})
            insights.append("Churn is healthy but monitor trends. Focus on onboarding quality.")
        elif churn_rate < 5.0:
            score -= 25
            benchmarks.append({"metric": "Monthly Churn", "value": f"{churn_rate:.2f}%", "status": "warning", "note": "Industry avg ~2.5%"})
            insights.append("⚠️ Churn is above average. Consider a win-back email campaign and in-app feedback surveys.")
        else:
            score -= 40
            benchmarks.append({"metric": "Monthly Churn", "value": f"{churn_rate:.2f}%", "status": "critical", "note": "Industry avg ~2.5%"})
            insights.append("🚨 High churn detected. Prioritize retention: exit surveys, pause subscriptions, cancellation flows.")

    # --- MRR Growth ---
    mrr_data = charts.get("mrr", {})
    mrr_growth = None
    if mrr_data and mrr_data.get("values") and len(mrr_data["values"]) >= 3:
        vals = [v["value"] for v in mrr_data["values"] if not v.get("incomplete")]
        if len(vals) >= 3:
            recent = vals[-1]
            three_months_ago = vals[-3]
            if three_months_ago > 0:
                mrr_growth = ((recent - three_months_ago) / three_months_ago) * 100

    if mrr_growth is not None:
        if mrr_growth > 20:
            benchmarks.append({"metric": "MRR Growth (3mo)", "value": f"+{mrr_growth:.1f}%", "status": "excellent", "note": "Strong growth"})
        elif mrr_growth > 5:
            benchmarks.append({"metric": "MRR Growth (3mo)", "value": f"+{mrr_growth:.1f}%", "status": "good", "note": "Healthy growth"})
        elif mrr_growth > 0:
            score -= 10
            benchmarks.append({"metric": "MRR Growth (3mo)", "value": f"+{mrr_growth:.1f}%", "status": "warning", "note": "Slow growth"})
            insights.append("📈 MRR growth is slow. Consider A/B testing pricing or adding a new tier.")
        else:
            score -= 25
            benchmarks.append({"metric": "MRR Growth (3mo)", "value": f"{mrr_growth:.1f}%", "status": "critical", "note": "MRR declining"})
            insights.append("🚨 MRR is declining. Investigate churn sources and consider a marketing push.")

    # --- Conversion Rate ---
    conv_data = charts.get("conversion_to_paying", {})
    conv_rate = None
    if conv_data and conv_data.get("summary"):
        conv_rate = conv_data["summary"].get("average", {}).get("Conversion Rate (7 days)")

    if conv_rate is not None:
        if conv_rate > 5:
            benchmarks.append({"metric": "Trial Conversion (7d)", "value": f"{conv_rate:.1f}%", "status": "excellent", "note": "Industry avg ~2-4%"})
        elif conv_rate > 2:
            benchmarks.append({"metric": "Trial Conversion (7d)", "value": f"{conv_rate:.1f}%", "status": "good", "note": "Industry avg ~2-4%"})
        elif conv_rate > 0.5:
            score -= 15
            benchmarks.append({"metric": "Trial Conversion (7d)", "value": f"{conv_rate:.1f}%", "status": "warning", "note": "Industry avg ~2-4%"})
            insights.append("💡 Trial conversion is below average. Try onboarding emails during trial or highlight premium features earlier.")
        else:
            score -= 30
            benchmarks.append({"metric": "Trial Conversion (7d)", "value": f"{conv_rate:.1f}%", "status": "critical", "note": "Industry avg ~2-4%"})
            insights.append("🚨 Very low trial conversion. Review your trial experience — are users reaching the 'aha moment'?")

    # --- Refund Rate ---
    refund_data = charts.get("refund_rate", {})
    refund_rate = None
    if refund_data and refund_data.get("summary"):
        refund_rate = refund_data["summary"].get("average", {}).get("Refund Rate")

    if refund_rate is not None:
        if refund_rate < 1.0:
            benchmarks.append({"metric": "Refund Rate", "value": f"{refund_rate:.2f}%", "status": "excellent", "note": "Industry avg ~2%"})
        elif refund_rate < 3.0:
            benchmarks.append({"metric": "Refund Rate", "value": f"{refund_rate:.2f}%", "status": "good", "note": "Industry avg ~2%"})
        else:
            score -= 15
            benchmarks.append({"metric": "Refund Rate", "value": f"{refund_rate:.2f}%", "status": "warning", "note": "Industry avg ~2%"})
            insights.append("⚠️ Refund rate is elevated. Check App Store reviews for recurring complaints.")

    if not insights:
        insights.append("✅ Your subscription metrics look healthy! Keep focused on growth and retention.")

    score = max(0, min(100, score))

    if score >= 80:
        grade = "A"
        label = "Excellent"
        color = "#10b981"
    elif score >= 60:
        grade = "B"
        label = "Good"
        color = "#3b82f6"
    elif score >= 40:
        grade = "C"
        label = "Needs Attention"
        color = "#f59e0b"
    else:
        grade = "D"
        label = "At Risk"
        color = "#ef4444"

    return {
        "score": score,
        "grade": grade,
        "label": label,
        "color": color,
        "insights": insights,
        "benchmarks": benchmarks,
    }
