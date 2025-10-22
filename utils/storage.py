from __future__ import annotations
import json
from pathlib import Path
from typing import Any, List, Dict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
PROJECTS_FILE = DATA_DIR / "projects.json"
TASKS_FILE = DATA_DIR / "tasks.json"

def _read_json(path: Path) -> list[dict]:
    """
    Read a JSON list from a file. If file missing or broken, return empty list.
    """
    try:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Ensure list
        return data if isinstance(data, list) else []
    except Exception:
        # In case of invalid JSON or other I/O errors
        return []

def _write_json(path: Path, data: list[dict]) -> None:
    """
    Write a list of dictionaries to a JSON file in a human-readable format.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_users() -> list[dict]:
    """Load raw user dicts."""
    return _read_json(USERS_FILE)

def save_users(users: list[dict]) -> None:
    """Save raw user dicts."""
    _write_json(USERS_FILE, users)

def load_projects() -> list[dict]:
    """Load raw project dicts."""
    return _read_json(PROJECTS_FILE)

def save_projects(projects: list[dict]) -> None:
    """Save raw project dicts."""
    _write_json(PROJECTS_FILE, projects)

def load_tasks() -> list[dict]:
    """Load raw task dicts."""
    return _read_json(TASKS_FILE)

def save_tasks(tasks: list[dict]) -> None:
    """Save raw task dicts."""
    _write_json(TASKS_FILE, tasks)