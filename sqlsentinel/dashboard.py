from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from .scope import validate_target, ScopeError
from .scanner import Scanner
from .reporting import write_report

console = Console()

def run_dashboard():
    console.print(Panel.fit("[bold cyan]SQLSentinel[/bold cyan]\nAuthorized SQL injection auditing dashboard",
                            border_style="cyan"))
    url = Prompt.ask("Target URL")
    host = Prompt.ask("Exact scope hostname (no scheme or path)")
    authorized = Confirm.ask("Do you have explicit written authorization for this exact host?",
                             default=False)
    allow_public = Confirm.ask("Is this a public host included in that authorization?",
                               default=False)
    try:
        checked_host, _ = validate_target(url, host, authorized, allow_public)
    except ScopeError as exc:
        console.print(f"[red]Scope rejected:[/red] {exc}")
        return
    max_requests = IntPrompt.ask("Maximum requests (1-50)", default=12)
    max_requests = max(1, min(50, max_requests))
    console.print("[yellow]Scanning sequentially. No data extraction or write operations are performed.[/yellow]")
    scanner = Scanner(max_requests=max_requests)
    report = scanner.scan(url, checked_host)
    table = Table(title="Audit results")
    table.add_column("Severity")
    table.add_column("Finding")
    table.add_column("Parameter")
    for f in report.findings:
        table.add_row(f.severity.upper(), f.title, f.parameter or "-")
    console.print(table)
    console.print(f"Requests sent: {report.requests_sent}")
    if Confirm.ask("Save an HTML report?", default=True):
        path = write_report(report, "html", Prompt.ask("Output path", default="reports/report.html"))
        console.print(f"[green]Saved:[/green] {path}")

