# File: packages/cli/udicti_cli/utils.py
import requests
from datetime import datetime
from rich.console import Console

console = Console()

# Point to your Render backend
BACKEND_API = "https://udicti-cli.onrender.com/api"

def log_event(event: str, data: dict = None):
    """Send anonymous usage event to your secure backend"""
    try:
        payload = {
            "event": event,
            "timestamp": datetime.now(datetime.UTC),
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