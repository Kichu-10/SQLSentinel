import json
import typer
from rich.console import Console
from rich.table import Table
from . import __version__
from .scope import validate_target, ScopeError
from .scanner import Scanner
from .reporting import write_report
from .dashboard import run_dashboard

app = typer.Typer(no_args_is_help=True, help="Scope-controlled SQL injection auditing.")
console = Console()

@app.command()
def version():
    """Show version."""
    console.print(f"SQLSentinel {__version__}")

@app.command("modules")
def modules():
    """List enabled, non-destructive modules."""
    table = Table("Module", "Purpose")
    for name, purpose in [
        ("url-query-parser", "Identify existing query parameters"),
        ("database-error-signatures", "Detect common DB error leakage"),
        ("boolean-differential", "Compare paired true/false responses"),
        ("waf-indicators", "Flag common block/rate-limit responses"),
        ("reporting", "JSON, HTML and text reports"),
    ]:
        table.add_row(name, purpose)
    console.print(table)

@app.command("inspect-url")
def inspect_url(url: str = typer.Argument(..., help="URL to inspect without sending requests.")):
    """Parse a URL and list its query parameter names without making a request."""
    from urllib.parse import urlparse, parse_qsl
    p = urlparse(url)
    if p.scheme not in ("http", "https") or not p.hostname:
        raise typer.BadParameter("Provide an absolute http(s) URL.")
    params = list(dict.fromkeys(k for k, _ in parse_qsl(p.query, keep_blank_values=True)))
    console.print(f"Host: {p.hostname}")
    console.print(f"Path: {p.path or '/'}")
    console.print("Parameters: " + (", ".join(params) if params else "(none)"))

@app.command()
def scan(
    url: str = typer.Argument(..., help="Exact target URL."),
    authorized: bool = typer.Option(False, "--authorized", help="Confirm written authorization."),
    scope_host: str = typer.Option(..., "--scope-host", help="Exact allowed hostname."),
    allow_public_target: bool = typer.Option(False, "--allow-public-target", help="Permit a public host covered by written authorization."),
    max_requests: int = typer.Option(12, min=1, max=50, help="Hard request cap."),
    delay: float = typer.Option(1.0, min=0.5, max=30.0, help="Delay between requests, seconds."),
    timeout: float = typer.Option(8.0, min=1.0, max=30.0, help="Per-request timeout."),
    output: str = typer.Option("reports/sqlsentinel-report.json", help="Report output path."),
    format: str = typer.Option("json", help="Report format: json, html, or txt."),
):
    """Run bounded, non-destructive checks on an authorized URL."""
    if format not in ("json", "html", "txt"):
        raise typer.BadParameter("Format must be json, html, or txt.")
    try:
        host, _ = validate_target(url, scope_host, authorized, allow_public_target)
    except ScopeError as exc:
        console.print(f"[bold red]Scope rejected:[/bold red] {exc}")
        raise typer.Exit(code=2)
    console.print(f"[cyan]SQLSentinel {__version__}[/cyan] · target={host} · max_requests={max_requests}")
    console.print("[yellow]Active checks are limited to non-destructive indicators. No extraction or writes.[/yellow]")
    try:
        report = Scanner(max_requests=max_requests, delay=delay, timeout=timeout).scan(url, host)
    except Exception as exc:
        console.print(f"[red]Scan failed:[/red] {exc}")
        raise typer.Exit(code=1)
    table = Table(title="Findings")
    table.add_column("Severity")
    table.add_column("Category")
    table.add_column("Parameter")
    table.add_column("Title")
    for f in report.findings:
        table.add_row(f.severity.upper(), f.category, f.parameter or "-", f.title)
    console.print(table)
    console.print(f"Requests sent: {report.requests_sent}")
    path = write_report(report, format, output)
    console.print(f"[green]Report saved:[/green] {path}")

@app.command()
def dashboard():
    """Launch the interactive terminal dashboard."""
    run_dashboard()

if __name__ == "__main__":
    app()
