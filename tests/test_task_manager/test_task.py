import pytest
from src.task_manager.task import Task, Priority


class TestTask:
    def test_create_task_with_defaults(self):
        task = Task("Тестовая задача")
        assert task.name == "Тестовая задача"
        assert task.description == ""
        assert task.completed is False
        assert task.priority == Priority.MEDIUM

    def test_create_task_with_all_params(self):
        task = Task("Важная", "Описание", priority=Priority.HIGH)
        assert task.name == "Важная"
        assert task.description == "Описание"
        assert task.priority == Priority.HIGH

    def test_custom_priority_low(self):
        task = Task("Низкая", priority=Priority.LOW)
        assert task.priority == Priority.LOW

    def test_custom_priority_high(self):
        task = Task("Высокая", priority=Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_invalid_priority_raises_ValueError(self):
        with pytest.raises(ValueError):
            Task("Баг", priority=15)

    def test_invalid_priority_zero_raises(self):
        with pytest.raises(ValueError):
            Task("Баг", priority=0)

    def test_invalid_priority_negative_raises(self):
        with pytest.raises(ValueError):
            Task("Баг", priority=-1)

    def test_priority_boundary_low(self):
        task = Task("Граница", priority=1)
        assert task.priority == 1

    def test_priority_boundary_high(self):
        task = Task("Граница", priority=10)
        assert task.priority == 10

    def test_priority_not_int_raises_TypeError(self):
        with pytest.raises(TypeError):
            Task("Баг", priority="высокий")

    def test_mark_complete(self):
        task = Task("К выполнению")
        assert task.completed is False
        task.complete()
        assert task.completed is True

    def test_complete_idempotent(self):
        task = Task("Тест")
        task.complete()
        task.complete()  # не должно менять
        assert task.completed is True

    def test_repr_contains_name(self):
        task = Task("Моя задача")
        assert "Моя задача" in repr(task)

    def test_repr_contains_priority(self):
        task = Task("Тест", priority=Priority.HIGH)
        assert "10" in repr(task)

    def test_repr_uncompleted(self):
        task = Task("Тест")
        assert "○" in repr(task)

    def test_repr_completed(self):
        task = Task("Тест")
        task.complete()
        assert "✓" in repr(task)