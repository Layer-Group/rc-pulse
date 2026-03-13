"""rc-pulse CLI entrypoint."""
import sys
import webbrowser
import tempfile
import os
import click
from .api import RevenueCatClient
from .health import calculate_health_score
from .report import generate_report

BANNER = r"""
  ____   ____       ____  _   _ _     ____  _____
 |  _ \ / ___|     |  _ \| | | | |   / ___|| ____|
 | |_) | |   ______| |_) | | | | |   \___ \|  _|
 |  _ <| |__|______|  __/| |_| | |___ ___) | |___
 |_| \_\\____|     |_|    \___/|_____|____/|_____|

 RevenueCat Charts API → Subscription Health Reports
 ─────────────────────────────────────────────────
"""


@click.group()
def cli():
    """rc-pulse: Turn your RevenueCat data into actionable health reports."""
    pass


@cli.command()
@click.option("--api-key", "-k", required=True, envvar="RC_API_KEY", help="RevenueCat V2 API key (or set RC_API_KEY env var)")
@click.option("--project-id", "-p", envvar="RC_PROJECT_ID", help="Project ID (or set RC_PROJECT_ID). Auto-detected if omitted.")
@click.option("--output", "-o", default=None, help="Output HTML file path. Opens in browser if omitted.")
@click.option("--no-open", is_flag=True, help="Don't open report in browser.")
def report(api_key, project_id, output, no_open):
    """Generate a subscription health report from RevenueCat Charts API data."""
    click.echo(BANNER)

    client = RevenueCatClient(api_key)

    # Auto-detect project
    if not project_id:
        click.echo("🔍 Auto-detecting project...")
        try:
            projects = client.get_projects()
            if not projects:
                click.echo("❌ No projects found for this API key.", err=True)
                sys.exit(1)
            if len(projects) > 1:
                click.echo("Multiple projects found:")
                for i, p in enumerate(projects):
                    click.echo(f"  [{i+1}] {p['name']} ({p['id']})")
                idx = click.prompt("Select project", type=int, default=1) - 1
                project_id = projects[idx]["id"]
                app_name = projects[idx]["name"]
            else:
                project_id = projects[0]["id"]
                app_name = projects[0]["name"]
            click.echo(f"✅ Using project: {app_name} ({project_id})")
        except Exception as e:
            click.echo(f"❌ Failed to fetch projects: {e}", err=True)
            sys.exit(1)
    else:
        app_name = project_id

    # Fetch overview
    click.echo("📊 Fetching overview metrics...")
    try:
        overview = client.get_overview(project_id)
        metrics = {m["id"]: m["value"] for m in overview.get("metrics", [])}
        mrr = metrics.get("mrr", 0)
        subs = metrics.get("active_subscriptions", 0)
        click.echo(f"   MRR: ${mrr:,.0f} | Active Subs: {subs:,}")
    except Exception as e:
        click.echo(f"❌ Failed to fetch overview: {e}", err=True)
        sys.exit(1)

    # Fetch charts
    click.echo("📈 Fetching chart data (this may take a moment)...")
    charts = client.get_all_charts(project_id)
    click.echo(f"   Loaded {len(charts)} charts")

    # Calculate health
    click.echo("🏥 Calculating health score...")
    health = calculate_health_score(charts, overview)
    click.echo(f"   Score: {health['score']}/100 ({health['grade']} — {health['label']})")

    # Generate report
    click.echo("✨ Generating HTML report...")
    html = generate_report(app_name, overview, charts, health)

    if output:
        with open(output, "w") as f:
            f.write(html)
        click.echo(f"\n✅ Report saved to: {output}")
        if not no_open:
            webbrowser.open(f"file://{os.path.abspath(output)}")
    else:
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
            f.write(html)
            tmp = f.name
        click.echo(f"\n✅ Opening report in browser...")
        webbrowser.open(f"file://{tmp}")
        click.echo(f"   (Temp file: {tmp})")

    click.echo("\n🦊 Report complete! Powered by rc-pulse.")


@cli.command()
@click.option("--api-key", "-k", required=True, envvar="RC_API_KEY", help="RevenueCat V2 API key")
def projects(api_key):
    """List all projects for an API key."""
    client = RevenueCatClient(api_key)
    try:
        projs = client.get_projects()
        if not projs:
            click.echo("No projects found.")
            return
        click.echo(f"Found {len(projs)} project(s):\n")
        for p in projs:
            click.echo(f"  📦 {p['name']}")
            click.echo(f"     ID: {p['id']}")
            click.echo()
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


def main():
    cli()


if __name__ == "__main__":
    main()
