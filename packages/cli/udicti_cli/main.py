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
from udicti_cli.utils import log_event, api_request

console = Console()


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