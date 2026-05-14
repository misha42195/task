from dataclasses import dataclass, field
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 5
    HIGH = 10


@dataclass
class Task:
    name: str
    description: str = ""
    priority: int = Priority.MEDIUM
    completed: bool = field(default=False)

    def __post_init__(self) -> None:
        if not isinstance(self.priority, int):
            raise TypeError("Приоритет должен быть числом")
        if not (1 <= self.priority <= 10):
            raise ValueError("Приоритет от 1 до 10")

    def complete(self) -> None:
        self.completed = True

    def __repr__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"Task({self.name!r}, priority={self.priority}, {status})"


if __name__ == "__main__":
    t1 = Task("задание1", "Простая задача")
    t2 = Task("срочное", priority=Priority.HIGH)
