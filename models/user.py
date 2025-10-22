from __future__ import annotations
from typing import ClassVar

class User:
    """
    - id: auto-incremented integer
    - name: display name
    - email: optional email
    """
    _id_counter: ClassVar[int] = 1

    def __init__(self, name: str, email: str | None = None) -> None:
        self._id = User._id_counter
        User._id_counter += 1

        self._name = name
        self._email = email

    @property
    def id(self) -> int:
        """Read-only id property."""
        return self._id

    @property
    def name(self) -> str:
        """Getter for name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Setter for name with guard."""
        if not value:
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def email(self) -> str | None:
        """Getter for email."""
        return self._email

    @email.setter
    def email(self, value: str | None) -> None:
        """Setter for email."""
        self._email = value

    def to_dict(self) -> dict:
        """Serialize to a plain dict (for JSON)."""
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """
        Create a User from a dict.
        Note: we also adjust _id_counter to keep it in sync.
        """
        obj = cls(name=data.get("name", ""), email=data.get("email"))
        # Overwrite auto id with stored id
        stored_id = data.get("id")
        if isinstance(stored_id, int):
            obj._id = stored_id
            if stored_id >= cls._id_counter:
                cls._id_counter = stored_id + 1
        return obj

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name!r}, email={self.email!r})"