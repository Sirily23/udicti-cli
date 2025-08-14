# File: packages/cli/udicti_cli/ui/theme.py

"""
UDICTI CLI UI Theme Components
Provides consistent styling, colors, and UI components across the entire application.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from typing import List, Dict, Any


# UDICTI Brand Colors
class Colors:
    PRIMARY = "#0864af"  # UDICTI Blue
    SECONDARY = "#f6b418"  # UDICTI Gold
    SUCCESS = "#22c55e"  # Green
    WARNING = "#f59e0b"  # Amber
    ERROR = "#ef4444"  # Red
    INFO = "#3b82f6"  # Blue
    MUTED = "#6b7280"  # Gray
    WHITE = "#ffffff"

    # Text variants
    PRIMARY_TEXT = "blue3"
    SUCCESS_TEXT = "green"
    WARNING_TEXT = "yellow"
    ERROR_TEXT = "red"
    MUTED_TEXT = "dim"


class Icons:
    """Consistent emoji icons used throughout the application"""

    ROCKET = "🚀"
    CHECK = "✅"
    WARNING = "⚠️"
    ERROR = "❌"
    INFO = "ℹ️"
    LOADING = "⏳"
    SEARCH = "🔍"
    SAVE = "💾"
    CELEBRATION = "🎉"
    KEY = "🔐"
    TROPHY = "🏆"
    DEVELOPER = "🧑‍💻"
    PENCIL = "📝"
    MOBILE = "📱"


class UdictiTheme:
    """Main theme class with reusable UI components"""

    def __init__(self):
        self.console = Console()

    def success_panel(self, message: str, title: str = "Success") -> Panel:
        """Create a success panel with consistent styling"""
        return Panel(
            Text.from_markup(
                f"[bold {Colors.SUCCESS_TEXT}]{Icons.CHECK} {message}[/bold {Colors.SUCCESS_TEXT}]"
            ),
            title=f"[bold white]{title}[/bold white]",
            border_style=Colors.SUCCESS_TEXT,
            padding=(1, 2),
        )

    def error_panel(self, message: str, title: str = "Error") -> Panel:
        """Create an error panel with consistent styling"""
        return Panel(
            Text.from_markup(
                f"[bold {Colors.ERROR_TEXT}]{Icons.ERROR} {message}[/bold {Colors.ERROR_TEXT}]"
            ),
            title=f"[bold white]{title}[/bold white]",
            border_style=Colors.ERROR_TEXT,
            padding=(1, 2),
        )

    def warning_panel(self, message: str, title: str = "Warning") -> Panel:
        """Create a warning panel with consistent styling"""
        return Panel(
            Text.from_markup(
                f"[bold {Colors.WARNING_TEXT}]{Icons.WARNING} {message}[/bold {Colors.WARNING_TEXT}]"
            ),
            title=f"[bold white]{title}[/bold white]",
            border_style=Colors.WARNING_TEXT,
            padding=(1, 2),
        )

    def info_panel(self, message: str, title: str = "Information") -> Panel:
        """Create an info panel with consistent styling"""
        return Panel(
            Text.from_markup(
                f"[bold {Colors.PRIMARY_TEXT}]{Icons.INFO} {message}[/bold {Colors.PRIMARY_TEXT}]"
            ),
            title=f"[bold white]{title}[/bold white]",
            border_style=Colors.PRIMARY_TEXT,
            padding=(1, 2),
        )

    def welcome_panel(self, message: str, title: str = "UDICTI CLI") -> Panel:
        """Create a branded welcome panel"""
        return Panel(
            Text.from_markup(message),
            title=f"[bold white]{title}[/bold white]",
            border_style=Colors.SECONDARY,
            padding=(1, 2),
        )

    def developers_table(
        self, developers: List[Dict[str, Any]], title: str = "UDICTI Developer Roster"
    ) -> Table:
        """Create a consistently styled developers table"""
        table = Table(
            title=f"[bold white]{Icons.DEVELOPER} {title}[/bold white]",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Name", style=Colors.PRIMARY_TEXT, no_wrap=True)
        table.add_column("GitHub", style=Colors.WARNING_TEXT, no_wrap=True)
        table.add_column("Skills", style=Colors.MUTED_TEXT, max_width=30)

        for dev in developers:
            skills_display = ", ".join(dev.get("skills", [])[:3])
            if len(dev.get("skills", [])) > 3:
                skills_display += "..."

            table.add_row(
                dev["name"], f"@{dev['github']}", skills_display or "No skills listed"
            )

        return table

    def loading_progress(self, description: str = "Loading..."):
        """Create a consistent loading progress indicator"""
        return Progress(
            SpinnerColumn(),
            TextColumn(f"[progress.description]{description}"),
            console=self.console,
            transient=True,
        )

    def prompt_with_style(self, question: str, default: Any = None) -> str:
        """Styled prompt with consistent theming"""
        styled_question = (
            f"[bold {Colors.PRIMARY_TEXT}]{question}[/bold {Colors.PRIMARY_TEXT}]"
        )
        return Prompt.ask(styled_question, default=default)

    def confirm_with_style(self, question: str, default: bool = True) -> bool:
        """Styled confirmation with consistent theming"""
        styled_question = (
            f"[bold {Colors.PRIMARY_TEXT}]{question}[/bold {Colors.PRIMARY_TEXT}]"
        )
        return Confirm.ask(styled_question, default=default)

    def print_step(self, step: str, description: str = ""):
        """Print a step with consistent styling"""
        step_text = f"[bold {Colors.PRIMARY_TEXT}]{step}[/bold {Colors.PRIMARY_TEXT}]"
        if description:
            step_text += f" {description}"
        self.console.print(step_text)

    def print_loading(self, message: str):
        """Print a loading message with consistent styling"""
        self.console.print(
            f"[{Colors.MUTED_TEXT}]{Icons.LOADING} {message}[/{Colors.MUTED_TEXT}]"
        )

    def print_success(self, message: str):
        """Print a success message with consistent styling"""
        self.console.print(
            f"[bold {Colors.SUCCESS_TEXT}]{Icons.CHECK} {message}[/bold {Colors.SUCCESS_TEXT}]"
        )

    def print_error(self, message: str):
        """Print an error message with consistent styling"""
        self.console.print(
            f"[bold {Colors.ERROR_TEXT}]{Icons.ERROR} {message}[/bold {Colors.ERROR_TEXT}]"
        )


# Global theme instance
theme = UdictiTheme()
