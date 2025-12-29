"""Tests for TaskStorage CRUD operations."""


from src.models import TaskCreate, TaskUpdate
from src.storage import TaskStorage


class TestTaskStorageInit:
    """Tests for TaskStorage initialization."""

    def test_empty_storage(self, storage: TaskStorage) -> None:
        """Test that new storage is empty."""
        assert storage.get_all() == []

    def test_next_id_starts_at_1(self, storage: TaskStorage) -> None:
        """Test that IDs start at 1."""
        task = storage.add(TaskCreate(title="Test"))
        assert task.id == 1


class TestTaskStorageAdd:
    """Tests for TaskStorage.add() method."""

    def test_add_task(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test adding a task."""
        task = storage.add(sample_task_create)
        assert task.id == 1
        assert task.title == sample_task_create.title
        assert task.description == sample_task_create.description
        assert task.completed is False

    def test_add_multiple_tasks_increments_id(self, storage: TaskStorage) -> None:
        """Test that IDs auto-increment."""
        task1 = storage.add(TaskCreate(title="Task 1"))
        task2 = storage.add(TaskCreate(title="Task 2"))
        task3 = storage.add(TaskCreate(title="Task 3"))
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_sets_timestamps(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test that timestamps are set on creation."""
        task = storage.add(sample_task_create)
        assert task.created_at is not None
        assert task.updated_at is not None


class TestTaskStorageGet:
    """Tests for TaskStorage.get() method."""

    def test_get_existing_task(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test getting an existing task by ID."""
        added = storage.add(sample_task_create)
        retrieved = storage.get(added.id)
        assert retrieved is not None
        assert retrieved.id == added.id
        assert retrieved.title == added.title

    def test_get_nonexistent_task(self, storage: TaskStorage) -> None:
        """Test getting a task that doesn't exist."""
        result = storage.get(999)
        assert result is None


class TestTaskStorageGetAll:
    """Tests for TaskStorage.get_all() method."""

    def test_get_all_empty(self, storage: TaskStorage) -> None:
        """Test get_all on empty storage."""
        assert storage.get_all() == []

    def test_get_all_with_tasks(self, storage_with_tasks: TaskStorage) -> None:
        """Test get_all returns all tasks."""
        tasks = storage_with_tasks.get_all()
        assert len(tasks) == 3

    def test_get_all_sorted_by_id(self, storage_with_tasks: TaskStorage) -> None:
        """Test that get_all returns tasks sorted by ID."""
        tasks = storage_with_tasks.get_all()
        ids = [t.id for t in tasks]
        assert ids == sorted(ids)


class TestTaskStorageUpdate:
    """Tests for TaskStorage.update() method."""

    def test_update_title(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test updating task title."""
        task = storage.add(sample_task_create)
        updated = storage.update(task.id, TaskUpdate(title="New title"))
        assert updated is not None
        assert updated.title == "New title"
        assert updated.description == sample_task_create.description

    def test_update_description(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test updating task description."""
        task = storage.add(sample_task_create)
        updated = storage.update(task.id, TaskUpdate(description="New description"))
        assert updated is not None
        assert updated.description == "New description"
        assert updated.title == sample_task_create.title

    def test_update_both_fields(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test updating both title and description."""
        task = storage.add(sample_task_create)
        updated = storage.update(
            task.id, TaskUpdate(title="New title", description="New description")
        )
        assert updated is not None
        assert updated.title == "New title"
        assert updated.description == "New description"

    def test_update_nonexistent_task(self, storage: TaskStorage) -> None:
        """Test updating a task that doesn't exist."""
        result = storage.update(999, TaskUpdate(title="New title"))
        assert result is None

    def test_update_updates_timestamp(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test that update modifies updated_at timestamp."""
        task = storage.add(sample_task_create)
        original_updated = task.updated_at
        updated = storage.update(task.id, TaskUpdate(title="New title"))
        assert updated is not None
        assert updated.updated_at >= original_updated

    def test_update_no_changes(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test update with no actual changes."""
        task = storage.add(sample_task_create)
        result = storage.update(task.id, TaskUpdate())
        assert result is not None
        assert result.title == task.title
        assert result.description == task.description


class TestTaskStorageDelete:
    """Tests for TaskStorage.delete() method."""

    def test_delete_existing_task(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test deleting an existing task."""
        task = storage.add(sample_task_create)
        deleted = storage.delete(task.id)
        assert deleted is not None
        assert deleted.id == task.id
        assert storage.get(task.id) is None

    def test_delete_nonexistent_task(self, storage: TaskStorage) -> None:
        """Test deleting a task that doesn't exist."""
        result = storage.delete(999)
        assert result is None

    def test_delete_removes_from_get_all(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test that deleted task is not in get_all."""
        task = storage.add(sample_task_create)
        storage.delete(task.id)
        tasks = storage.get_all()
        assert len(tasks) == 0


class TestTaskStorageMarkComplete:
    """Tests for TaskStorage.mark_complete() method."""

    def test_mark_complete_pending_task(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test marking a pending task as complete."""
        task = storage.add(sample_task_create)
        assert task.completed is False
        completed = storage.mark_complete(task.id)
        assert completed is not None
        assert completed.completed is True

    def test_mark_complete_already_completed(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test marking an already completed task."""
        task = storage.add(sample_task_create)
        storage.mark_complete(task.id)
        result = storage.mark_complete(task.id)
        assert result is not None
        assert result.completed is True

    def test_mark_complete_nonexistent_task(self, storage: TaskStorage) -> None:
        """Test marking a nonexistent task as complete."""
        result = storage.mark_complete(999)
        assert result is None

    def test_mark_complete_updates_timestamp(
        self, storage: TaskStorage, sample_task_create: TaskCreate
    ) -> None:
        """Test that mark_complete updates the timestamp."""
        task = storage.add(sample_task_create)
        original_updated = task.updated_at
        completed = storage.mark_complete(task.id)
        assert completed is not None
        assert completed.updated_at >= original_updated
