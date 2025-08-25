# File: packages/cli/udicti_cli/main.py

"""
This is the main entry point for the udicti cli application.
It serves as the central router, importing all command modules and
making them accessible to the user via the `typer` framework.
"""
import typer
from rich.console import Console
import requests
from datetime import datetime
import os

# Import all command modules
from udicti_cli.commands import welcome
from udicti_cli.commands import onboarding
from udicti_cli.commands import show
from udicti_cli.commands import github_auth
from udicti_cli.commands import dashboard

console = Console()

# Point to your Render backend
BACKEND_API = "https://udicti-cli.onrender.com/api"

def log_event(event: str, data: dict = None):
    """Send anonymous usage event to your secure backend"""
    try:
        payload = {
            "event": event,
            "timestamp":  datetime.datetime.now(datetime.UTC),
            "source": "cli",
            "data": data or {}
        }
        # Non-blocking, fast timeout
        requests.post(f"{BACKEND_API}/log", json=payload, timeout=3)
    except:
        pass  # Silent fail — UX first

def api_request(endpoint: str, method: str = "GET", data: dict = None):
    """Make API request to backend"""
    try:
        url = f"{BACKEND_API}/{endpoint}"
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]Error connecting to UDICTI backend: {e}[/bold red]")
        return None

# Create the main Typer application object
app = typer.Typer(
    help="UDICTI CLI a modern and simple developers analytics and workflow tool to be used by devs, odds are this tool will be used to simplfy workflows and faster speed for your projects"
)

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    The main callback for the CLI. Displays a welcome message and banner if no
    subcommand is specified.
    """
    # Log CLI startup
    log_event("cli_startup", {"subcommand": ctx.invoked_subcommand})

    # If no subcommand was provided by the user, display the welcome banner.
    if ctx.invoked_subcommand is None:
        welcome.show_welcome()
        log_event("welcome_shown")

app.add_typer(welcome.app, name="welcome")
app.add_typer(onboarding.onboarding_app)
app.add_typer(show.show_app, name="show")
app.add_typer(github_auth.github_auth_app, name="github-auth")
app.add_typer(dashboard.dashboard_app, name="dashboard")

# This block ensures that the Typer application runs when the script is executed directly.
if __name__ == "__main__":
    app()