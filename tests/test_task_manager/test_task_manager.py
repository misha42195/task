import pytest
from src.task_manager.task import Task, Priority
from src.task_manager.task_manager import TaskManager


@pytest.fixture
def manager():
    return TaskManager()


@pytest.fixture
def sample_tasks():
    return [
        Task("Задача 1", priority=Priority.LOW),
        Task("Задача 2", priority=Priority.MEDIUM),
        Task("Срочная", priority=Priority.HIGH),
    ]


class TestTaskManagerInit:
    def test_empty_manager(self):
        tm = TaskManager()
        assert len(tm) == 0

    def test_empty_manager_all(self):
        tm = TaskManager()
        assert tm.all() == []

    def test_empty_manager_iter(self):
        tm = TaskManager()
        assert list(tm) == []


class TestTaskManagerAdd:
    def test_add_single_task(self, manager):
        task = Task("Новая")
        manager.add(task)
        assert len(manager) == 1

    def test_add_multiple_tasks(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        assert len(manager) == 3

    def test_add_duplicate_raises(self, manager):
        manager.add(Task("Дубликат"))
        with pytest.raises(ValueError, match="уже существует"):
            manager.add(Task("Дубликат"))

    def test_add_wrong_type_raises(self, manager):
        with pytest.raises(TypeError):
            manager.add("не задача")

    def test_add_task_is_retrievable(self, manager):
        task = Task("Добавил", priority=Priority.HIGH)
        manager.add(task)
        retrieved = manager.get("Добавил")
        assert retrieved is task


class TestTaskManagerGet:
    def test_get_existing(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        result = manager.get("Срочная")
        assert result is not None
        assert result.name == "Срочная"

    def test_get_nonexistent_returns_none(self, manager):
        result = manager.get("Не существует")
        assert result is None

    def test_get_with_string(self, manager):
        manager.add(Task("Поиск"))
        assert manager.get("Поиск").priority == Priority.MEDIUM


class TestTaskManagerRemove:
    def test_remove_existing(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        result = manager.remove("Задача 1")
        assert result is True
        assert len(manager) == 2
        assert manager.get("Задача 1") is None

    def test_remove_nonexistent_returns_false(self, manager):
        result = manager.remove("Нет такой")
        assert result is False

    def test_remove_decreases_count(self, manager):
        manager.add(Task("Удаляемая"))
        manager.remove("Удаляемая")
        assert len(manager) == 0


class TestTaskManagerIterate:
    def test_iterate_empty(self, manager):
        assert list(manager) == []

    def test_iterate_all_tasks(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        tasks = list(manager)
        assert len(tasks) == 3


class TestTaskManagerLen:
    def test_len_empty(self, manager):
        assert len(manager) == 0

    def test_len_after_add(self, manager):
        manager.add(Task("Раз"))
        manager.add(Task("Два"))
        assert len(manager) == 2


class TestTaskManagerFilter:
    def test_all_returns_list(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        assert len(manager.all()) == 3

    def test_pending_only_uncompleted(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        sample_tasks[0].complete()
        pending = manager.pending()
        assert len(pending) == 2
        assert all(not t.completed for t in pending)

    def test_completed_only_completed(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        sample_tasks[1].complete()
        completed = manager.completed()
        assert len(completed) == 1
        assert all(t.completed for t in completed)

    def test_pending_empty_when_all_done(self, manager):
        for i in range(3):
            t = Task(f"Завершенная {i}")
            t.complete()
            manager.add(t)
        assert manager.pending() == []


class TestTaskManagerSort:
    def test_by_priority_descending(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        sorted_tasks = manager.by_priority()
        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[-1].priority == Priority.LOW

    def test_by_priority_ascending(self, manager, sample_tasks):
        for task in sample_tasks:
            manager.add(task)
        sorted_tasks = manager.by_priority(reverse=False)
        assert sorted_tasks[0].priority == Priority.LOW
        assert sorted_tasks[-1].priority == Priority.HIGH

    def test_by_priority_empty(self, manager):
        assert manager.by_priority() == []