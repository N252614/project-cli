from __future__ import annotations
import argparse
import re
from typing import List, Optional

from utils.printing import info, warn, error, table
from utils import storage

# Import model classes
from models.user import User
from models.project import Project
from models.task import Task

def _load_users_as_models() -> list[User]:
    """Load users.json and convert dicts to User models."""
    users_raw = storage.load_users()
    users: list[User] = []
    for d in users_raw:
        try:
            users.append(User.from_dict(d))
        except Exception:
            continue
    return users

def _load_projects_as_models() -> list[Project]:
    """Load projects.json and convert dicts to Project models."""
    projects_raw = storage.load_projects()
    projects: list[Project] = []
    for d in projects_raw:
        try:
            projects.append(Project.from_dict(d))
        except Exception:
            continue
    return projects

def _load_tasks_as_models() -> list[Task]:
    """Load tasks.json and convert dicts to Task models."""
    tasks_raw = storage.load_tasks()
    tasks: list[Task] = []
    for d in tasks_raw:
        try:
            tasks.append(Task.from_dict(d))
        except Exception:
            continue
    return tasks

def _save_projects_from_models(projects: list[Project]) -> None:
    """Serialize Project models to dicts and save to projects.json."""
    storage.save_projects([p.to_dict() for p in projects])

def _save_tasks_from_models(tasks: list[Task]) -> None:
    """Serialize Task models to dicts and save to tasks.json."""
    storage.save_tasks([t.to_dict() for t in tasks])    

def _find_user_by_name(users: list[User], name: str) -> Optional[User]:
    """Find user by name (case-insensitive)."""
    name_norm = name.strip().lower()
    for u in users:
        if u.name.strip().lower() == name_norm:
            return u
    return None

def _find_project_by_title(projects: list[Project], title: str) -> Optional[Project]:
    """Find project by title (case-insensitive)."""
    title_norm = title.strip().lower()
    for p in projects:
        if p.title.strip().lower() == title_norm:
            return p
    return None

def _is_iso_date(value: str) -> bool:
    """Simple check for date format YYYY-MM-DD."""
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))

def build_parser() -> argparse.ArgumentParser:
    """Define CLI structure and available subcommands."""
    parser = argparse.ArgumentParser(
        prog="project-cli",
        description=" CLI tool to manage users and projects."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add-user
    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name", required=True, help="User name")
    p_add_user.add_argument("--email", required=False, help="User email")

    # list-users
    subparsers.add_parser("list-users", help="List all users")

    # add-project
    p_add_project = subparsers.add_parser("add-project", help="Add project to a user")
    p_add_project.add_argument("--user", required=True, help="User name (owner of the project)")
    p_add_project.add_argument("--title", required=True, help="Project title")
    p_add_project.add_argument("--description", required=False, help="Project description")
    p_add_project.add_argument("--due-date", required=False, help="Due date in YYYY-MM-DD")

    # list-projects
    p_list_projects = subparsers.add_parser("list-projects", help="List projects (optionally by user)")
    p_list_projects.add_argument("--user", required=False, help="Filter by user name")

    # tasks
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True, help="Project title (exact)")
    p_add_task.add_argument("--title", required=True, help="Task title")
    p_add_task.add_argument("--assigned-to", required=False, help="User name to assign (optional)")

    p_list_tasks = subparsers.add_parser("list-tasks", help="List tasks (optionally by project)")
    p_list_tasks.add_argument("--project", required=False, help="Filter by project title")

    p_complete_task = subparsers.add_parser("complete-task", help="Mark a task as completed")
    p_complete_task.add_argument("--id", type=int, required=True, help="Task id")

    return parser

def cmd_add_user(name: str, email: str | None) -> None:
    """Add new user to JSON."""
    users = storage.load_users()
    new_id = (max([u.get("id", 0) for u in users]) + 1) if users else 1
    users.append({"id": new_id, "name": name, "email": email})
    storage.save_users(users)
    info(f"User created: id={new_id}, name='{name}'")

def cmd_list_users() -> None:
    """Display all users in table."""
    users = storage.load_users()
    if not users:
        warn("No users yet.")
        return
    rows = [[u.get("id"), u.get("name"), u.get("email") or "—"] for u in users]
    table ("Users", ["ID", "Name", "Email"], rows)

def cmd_add_project(user_name: str, title: str, description: str | None, due_date: str | None) -> None:
    """Add a new project assigned to a specific user."""
    users = _load_users_as_models()
    user = _find_user_by_name(users, user_name)
    if not user:
        error(f"User '{user_name}' not found. Create the user first with 'add-user'.")
        return

    if due_date and not _is_iso_date(due_date):
        warn("Due date is not in YYYY-MM-DD format. It will be stored as-is.")

    projects = _load_projects_as_models()
    project = Project(title=title, user_id=user.id, description=description, due_date=due_date)
    projects.append(project)
    _save_projects_from_models(projects)

    info(f"Project created: id={project.id}, title='{project.title}', owner='{user.name}'")

def cmd_list_projects(user_name: str | None) -> None:
    """List all projects or filter by user."""
    users = _load_users_as_models()
    user_by_id = {u.id: u for u in users}

    owner_filter_id: Optional[int] = None
    if user_name:
        user = _find_user_by_name(users, user_name)
        if not user:
            warn(f"No such user '{user_name}'.")
            table("Projects", ["ID", "Title", "Owner", "Due", "Description"], [])
            return
        owner_filter_id = user.id

    projects = _load_projects_as_models()
    if owner_filter_id is not None:
        projects = [p for p in projects if p.user_id == owner_filter_id]

    if not projects:
        warn("No projects yet.")
        return

    rows = []
    for p in projects:
        owner = user_by_id.get(p.user_id)
        owner_name = owner.name if owner else f"#{p.user_id}"
        rows.append([p.id, p.title, owner_name, p.due_date or "—", (p.description or "—")[:60]])

    table("Projects", ["ID", "Title", "Owner", "Due", "Description"], rows)

def cmd_add_task(project_title: str, title: str, assigned_to_name: str | None) -> None:
    """Create a task inside a project and optionally assign to a user."""
    projects = _load_projects_as_models()
    project = _find_project_by_title(projects, project_title)
    if not project:
        error(f"Project '{project_title}' not found.")
        return

    assigned_to = None
    if assigned_to_name:
        users = _load_users_as_models()
        user = _find_user_by_name(users, assigned_to_name)
        if not user:
            warn(f"User '{assigned_to_name}' not found. Task will be unassigned.")
        else:
            assigned_to = user.id

    tasks = _load_tasks_as_models()
    task = Task(project_id=project.id, title=title, assigned_to=assigned_to)
    tasks.append(task)
    _save_tasks_from_models(tasks)

    info(f"Task added: '{task.title}' for project '{project.title}'")


def cmd_list_tasks(project_title: str | None) -> None:
    """List tasks, optionally filter by project title."""
    tasks = _load_tasks_as_models()
    if not tasks:
        warn("No tasks yet.")
        return

    projects = _load_projects_as_models()
    users = _load_users_as_models()
    project_by_id = {p.id: p for p in projects}
    user_by_id = {u.id: u for u in users}

    if project_title:
        project = _find_project_by_title(projects, project_title)
        if not project:
            warn(f"No such project '{project_title}'.")
            return
        tasks = [t for t in tasks if t.project_id == project.id]

    if not tasks:
        warn("No tasks yet.")
        return

    rows = []
    for t in tasks:
        proj = project_by_id.get(t.project_id)
        assignee = user_by_id.get(t.assigned_to) if t.assigned_to else None
        rows.append([
            t.id,
            t.title,
            proj.title if proj else "?",
            assignee.name if assignee else "—",
            t.status
        ])
    table("Tasks", ["ID", "Title", "Project", "Assigned To", "Status"], rows)


def cmd_complete_task(task_id: int) -> None:
    """Mark task as done by id."""
    tasks = _load_tasks_as_models()
    found = False
    for t in tasks:
        if t.id == task_id:
            t.mark_done()
            found = True
            break

    if not found:
        error(f"No task with id={task_id}")
        return

    _save_tasks_from_models(tasks)
    info(f"Task #{task_id} marked as done!")

def main(argv: List[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add-user":
        cmd_add_user(args.name, args.email)
        return 0

    if args.command == "list-users":
        cmd_list_users()
        return 0

    if args.command == "add-project":
        cmd_add_project(args.user, args.title, args.description, args.due_date)
        return 0

    if args.command == "list-projects":
        cmd_list_projects(args.user)
        return 0

    if args.command == "add-task":
        cmd_add_task(args.project, args.title, args.assigned_to)
        return 0

    if args.command == "list-tasks":
        cmd_list_tasks(args.project)
        return 0

    if args.command == "complete-task":
        cmd_complete_task(args.id)
        return 0

    error("Unknown command.")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())