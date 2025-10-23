import subprocess
import json
import sys
from pathlib import Path

DATA_PATH = Path("data")

# Clean up old data files before running tests (fresh state)
for file_name in ["users.json", "projects.json", "tasks.json"]:
    f = DATA_PATH / file_name
    if f.exists():
        f.unlink()  # delete old file if it exists

def run_cli_args(args): # type: (list) -> subprocess.CompletedProcess
    """
    Run CLI using the *same* Python interpreter that runs pytest.
    This avoids 'python' vs 'python3' issues and wrong venv.
    """
    return subprocess.run(
        [sys.executable, "main.py", *args],
        capture_output=True,
        text=True
    )

def test_add_user_creates_entry():
    """Check that 'add-user' creates users.json and writes the user."""
    proc = run_cli_args(["add-user", "--name", "TestUser", "--email", "test@example.com"])
    assert proc.returncode == 0, f"CLI failed: {proc.stderr}\nSTDOUT:\n{proc.stdout}"

    users_file = DATA_PATH / "users.json"
    assert users_file.exists(), "users.json file does not exist"
    users = json.loads(users_file.read_text() or "[]")
    assert any(u.get("name") == "TestUser" for u in users), "User not found in users.json"

def test_add_project_creates_entry():
    """Check that 'add-project' creates a project for existing user."""
    proc = run_cli_args(["add-project", "--user", "TestUser", "--title", "Demo Project"])
    assert proc.returncode == 0, f"CLI failed: {proc.stderr}\nSTDOUT:\n{proc.stdout}"

    projects_file = DATA_PATH / "projects.json"
    assert projects_file.exists(), "projects.json file does not exist"
    projects = json.loads(projects_file.read_text() or "[]")
    assert any(p.get("title") == "Demo Project" for p in projects), "Project not found in projects.json"

def test_add_task_creates_entry():
    """Check that 'add-task' creates a task under the project and optional assignee."""
    proc = run_cli_args([
        "add-task",
        "--project", "Demo Project",
        "--title", "Check README",
        "--assigned-to", "TestUser",
    ])
    assert proc.returncode == 0, f"CLI failed: {proc.stderr}\nSTDOUT:\n{proc.stdout}"

    tasks_file = DATA_PATH / "tasks.json"
    assert tasks_file.exists(), "tasks.json file does not exist"
    tasks = json.loads(tasks_file.read_text() or "[]")
    assert any(t.get("title") == "Check README" for t in tasks), "Task not found in tasks.json"