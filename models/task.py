from __future__ import annotations
from typing import ClassVar

class Task:
    """
     Task model.
    - id: auto-increment
    - project_id: link to project (one-to-many: Project -> Tasks)
    - title: short task title
    - status: 'todo' | 'in-progress' | 'done'
    - assigned_to:  user id (assignee)
    """

    _id_counter: ClassVar[int] = 1
    VALID_STATUSES = {"todo", "in-progress", "done"}

    def __init__(self, project_id: int, title: str, status: str = "todo", assigned_to: int | None = None) -> None:
        # auto id
        self._id = Task._id_counter
        Task._id_counter += 1

        # basic fields
        self.project_id = project_id
        self.title = title
        self.status = status if status in self.VALID_STATUSES else "todo"
        self.assigned_to = assigned_to

    @property
    def id(self) -> int:
        """Read-only id."""
        return self._id

    def mark_done(self) -> None:
        """Set status to 'done'."""
        self.status = "done"

    def to_dict(self) -> dict:
        """Serialize to plain dict."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """
        Build Task from dict; also keep id counter in sync.
        """
        obj = cls(
            project_id=int(data.get("project_id", 0)),
            title=data.get("title", ""),
            status=data.get("status", "todo"),
            assigned_to=data.get("assigned_to"),
        )
        stored_id = data.get("id")
        if isinstance(stored_id, int):
            obj._id = stored_id
            if stored_id >= cls._id_counter:
                cls._id_counter = stored_id + 1
        return obj

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title={self.title!r}, status={self.status!r})"