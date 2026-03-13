"""RevenueCat Charts API v2 client."""
import requests
from typing import Optional

BASE_URL = "https://api.revenuecat.com/v2"

CHARTS = [
    "mrr", "arr", "actives", "actives_movement", "actives_new",
    "churn", "revenue", "customers_new", "conversion_to_paying",
    "mrr_movement", "trials", "refund_rate", "ltv_per_customer",
]


class RevenueCatClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def get_projects(self) -> list:
        r = self.session.get(f"{BASE_URL}/projects")
        r.raise_for_status()
        return r.json().get("items", [])

    def get_overview(self, project_id: str) -> dict:
        r = self.session.get(f"{BASE_URL}/projects/{project_id}/metrics/overview")
        r.raise_for_status()
        return r.json()

    def get_chart(self, project_id: str, chart: str) -> Optional[dict]:
        try:
            r = self.session.get(f"{BASE_URL}/projects/{project_id}/charts/{chart}")
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    def get_all_charts(self, project_id: str) -> dict:
        results = {}
        for chart in CHARTS:
            data = self.get_chart(project_id, chart)
            if data and "object" not in data or (data and data.get("object") != "error"):
                results[chart] = data
        return results
