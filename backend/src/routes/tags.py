"""Tags API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.dependencies import get_current_user_id
from src.database import get_session
from src.models.tag import Tag
from src.schemas.tag import TagCreate, TagResponse

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("", response_model=list[TagResponse])
async def get_tags(
    search: str | None = None,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> list[TagResponse]:
    """Get all tags for the current user with optional search.

    Args:
        search: Search prefix for autocomplete.
        user_id: Current user ID.
        session: Database session.

    Returns:
        List of tags.
    """
    query = select(Tag).where(Tag.user_id == user_id)

    if search:
        query = query.where(Tag.name.ilike(f"{search}%"))

    query = query.order_by(Tag.name.asc())

    result = await session.execute(query)
    tags = result.scalars().all()

    return [TagResponse.model_validate(tag) for tag in tags]


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TagResponse:
    """Create a new tag.

    Args:
        tag_data: Tag creation data.
        user_id: Current user ID.
        session: Database session.

    Returns:
        Created tag.

    Raises:
        HTTPException: If tag with same name already exists.
    """
    # Check for duplicate
    result = await session.execute(
        select(Tag).where(Tag.user_id == user_id, Tag.name == tag_data.name)
    )
    existing_tag = result.scalar_one_or_none()

    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tag with this name already exists",
        )

    tag = Tag(
        user_id=user_id,
        name=tag_data.name,
    )
    session.add(tag)
    await session.commit()
    await session.refresh(tag)

    return TagResponse.model_validate(tag)


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> TagResponse:
    """Get a single tag by ID.

    Args:
        tag_id: Tag ID.
        user_id: Current user ID.
        session: Database session.

    Returns:
        Tag details.

    Raises:
        HTTPException: If tag not found or unauthorized.
    """
    result = await session.execute(
        select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    )
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    return TagResponse.model_validate(tag)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a tag.

    Args:
        tag_id: Tag ID.
        user_id: Current user ID.
        session: Database session.

    Raises:
        HTTPException: If tag not found or unauthorized.
    """
    result = await session.execute(
        select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
    )
    tag = result.scalar_one_or_none()

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag not found",
        )

    await session.delete(tag)
    await session.commit()
