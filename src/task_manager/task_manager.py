from collections.abc import Iterator

from src.task_manager.task import Task


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add(self, task: Task) -> None:
        if not isinstance(task, Task):
            raise TypeError("Ожидался объект Task")
        if task.name in self._tasks:
            raise ValueError(f"Задача '{task.name}' уже существует")
        self._tasks[task.name] = task

    def get(self, name: str) -> Task | None:
        return self._tasks.get(name)

    def remove(self, name: str) -> bool:
        if name in self._tasks:
            del self._tasks[name]
            return True
        return False

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks.values())

    def __len__(self) -> int:
        return len(self._tasks)

    def all(self) -> list[Task]:
        return list(self._tasks.values())

    def pending(self) -> list[Task]:
        return [t for t in self if not t.completed]

    def completed(self) -> list[Task]:
        return [t for t in self if t.completed]

    def by_priority(self, reverse: bool = True) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.priority, reverse=reverse)


if __name__ == "__main__":
    tm = TaskManager()
    tm.add(Task("Задача 1", priority=3))
    tm.add(Task("Срочная", priority=10))

    for task in tm:
        print(task)