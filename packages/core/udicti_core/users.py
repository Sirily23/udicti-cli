import json
from pathlib import Path
import typer
from typing import List, Dict, Any


APP_NAME = "udicti-cli"
app_dir = Path(typer.get_app_dir(APP_NAME))
app_dir.mkdir(parents=True, exist_ok=True)
db_path = app_dir / "users.json"

def init_db():
    """Initializes the user database if it doesn't exist."""
    if not db_path.is_file():
        db_path.write_text("[]")

def get_users() -> List[Dict[str, Any]]:
    """Reads and returns all users from the database."""
    init_db()
    with db_path.open("r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def add_user(name: str, email: str, github: str) -> Dict[str, Any]:
    """Adds a new user to the database."""
    users = get_users()
    new_user = {"name": name, "email": email, "github": github}
    
    # Prevent duplicate entries based on email
    if any(user["email"] == email for user in users):
        raise ValueError(f"User with email {email} already exists.")
        
    users.append(new_user)
    
    with db_path.open("w") as f:
        json.dump(users, f, indent=4)
        
    return new_user