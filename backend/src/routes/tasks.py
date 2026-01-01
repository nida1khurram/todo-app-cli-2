"""Tasks API routes."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.dependencies import get_current_user_id
from src.database import get_session
from src.models.task import Task
from src.models.tag import Tag
from src.models.task_tag import TaskTag
from src.schemas.task import TaskCreate, TaskResponse, TaskUpdate


async def get_or_create_tags(
    session: AsyncSession,
    user_id: str,
    tag_names: list[str],
) -> list[Tag]:
    """Get existing tags or create new ones.

    Args:
        session: Database session.
        user_id: Current user ID.
        tag_names: List of tag names to get or create.

    Returns:
        List of Tag objects.
    """
    tags = []
    for name in tag_names:
        name = name.strip().lower()
        if not name:
            continue

        # Check if tag exists
        result = await session.execute(
            select(Tag).where(Tag.user_id == user_id, Tag.name == name)
        )
        tag = result.scalar_one_or_none()

        if not tag:
            # Create new tag
            tag = Tag(user_id=user_id, name=name)
            session.add(tag)
            await session.flush()  # Get the ID

        tags.append(tag)

    return tags


def task_to_response(task: Task) -> TaskResponse:
    """Convert Task model to TaskResponse with tags.

    Args:
        task: Task model instance.

    Returns:
        TaskResponse with tags list.
    """
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
        priority=task.priority,
        created_at=task.created_at,
        updated_at=task.updated_at,
        tags=[],  # Tags relationship removed for simplicity
    )

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskResponse])
async def get_tasks(
    status_filter: str | None = None,
    priority: str | None = None,
    search: str | None = None,
    tags: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> list[TaskResponse]:
    """Get all tasks for the current user with optional filters.

    Args:
        status_filter: Filter by completion status (all/completed/pending).
        priority: Filter by priority level.
        search: Search in title and description.
        tags: Comma-separated tag names to filter by.
        sort_by: Field to sort by.
        sort_order: Sort direction (asc/desc).
        user_id: Current user ID.
        session: Database session.

    Returns:
        List of tasks.
    """
    query = select(Task).where(Task.user_id == user_id)

    # Apply status filter
    if status_filter == "completed":
        query = query.where(Task.is_completed == True)  # noqa: E712
    elif status_filter == "pending":
        query = query.where(Task.is_completed == False)  # noqa: E712

    # Apply priority filter
    if priority and priority in ["high", "medium", "low"]:
        query = query.where(Task.priority == priority)

    # Apply search filter
    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            Task.title.ilike(search_pattern) | Task.description.ilike(search_pattern)
        )

    # Apply tag filter
    if tags:
        tag_names = [t.strip().lower() for t in tags.split(",") if t.strip()]
        if tag_names:
            # Join with task_tags and tags tables to filter
            query = query.join(TaskTag, Task.id == TaskTag.task_id).join(
                Tag, TaskTag.tag_id == Tag.id
            ).where(Tag.name.in_(tag_names))

    # Apply sorting
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    result = await session.execute(query)
    tasks = result.unique().scalars().all()

    return [task_to_response(task) for task in tasks]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Create a new task.

    Args:
        task_data: Task creation data.
        user_id: Current user ID.
        session: Database session.

    Returns:
        Created task.
    """
    task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
    )
    session.add(task)
    await session.flush()  # Get the task ID

    # Handle tags
    if task_data.tags:
        tags = await get_or_create_tags(session, user_id, task_data.tags)
        for tag in tags:
            task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
            session.add(task_tag)

    await session.commit()
    await session.refresh(task)

    return task_to_response(task)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Get a single task by ID.

    Args:
        task_id: Task ID.
        user_id: Current user ID.
        session: Database session.

    Returns:
        Task details.

    Raises:
        HTTPException: If task not found or unauthorized.
    """
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task_to_response(task)


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Update a task.

    Args:
        task_id: Task ID.
        task_data: Task update data.
        user_id: Current user ID.
        session: Database session.

    Returns:
        Updated task.

    Raises:
        HTTPException: If task not found or unauthorized.
    """
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update fields if provided
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field != "tags":  # Handle tags separately
            setattr(task, field, value)

    task.updated_at = datetime.utcnow()

    # Handle tags update if provided
    if task_data.tags is not None:
        # Delete existing task-tag associations
        await session.execute(
            select(TaskTag).where(TaskTag.task_id == task_id)
        )
        existing_task_tags = await session.execute(
            select(TaskTag).where(TaskTag.task_id == task_id)
        )
        for tt in existing_task_tags.scalars().all():
            await session.delete(tt)

        # Add new tags
        if task_data.tags:
            tags = await get_or_create_tags(session, user_id, task_data.tags)
            for tag in tags:
                task_tag = TaskTag(task_id=task.id, tag_id=tag.id)
                session.add(task_tag)

    await session.commit()
    await session.refresh(task)

    return task_to_response(task)


@router.patch("/{task_id}", response_model=TaskResponse)
async def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    """Toggle task completion status.

    Args:
        task_id: Task ID.
        user_id: Current user ID.
        session: Database session.

    Returns:
        Updated task.

    Raises:
        HTTPException: If task not found or unauthorized.
    """
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task_to_response(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a task.

    Args:
        task_id: Task ID.
        user_id: Current user ID.
        session: Database session.

    Raises:
        HTTPException: If task not found or unauthorized.
    """
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    await session.delete(task)
    await session.commit()
