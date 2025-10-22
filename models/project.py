from __future__ import annotations
from typing import ClassVar

class Project:
    """
   Project model.
    - id: auto-increment
    - title: project title
    - description: optional
    - due_date: ISO string (YYYY-MM-DD)
    - user_id: owner user id (one-to-many: User -> Projects)
    """

    _id_counter: ClassVar[int] = 1

    def __init__(self, title: str, user_id: int, description: str | None = None, due_date: str | None = None) -> None:
        self._id = Project._id_counter
        Project._id_counter += 1

        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_id = user_id

    @property
    def id(self) -> int:
        return self._id

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "user_id": self.user_id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        obj = cls(
            title=data.get("title", ""),
            user_id=int(data.get("user_id")) if data.get("user_id") is not None else 0,
            description=data.get("description"),
            due_date=data.get("due_date"),
        )
        stored_id = data.get("id")
        if isinstance(stored_id, int):
            obj._id = stored_id
            if stored_id >= cls._id_counter:
                cls._id_counter = stored_id + 1
        return obj

    def __repr__(self) -> str:
        return f"Project(id={self.id}, title={self.title!r}, user_id={self.user_id})"