"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.auth.dependencies import get_current_user
from src.auth.jwt import create_access_token
from src.auth.password import hash_password, verify_password
from src.database import get_session
from src.models.user import User
from src.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Register a new user account.

    Args:
        user_data: User registration data (email, password).
        session: Database session.

    Returns:
        JWT token and user info.

    Raises:
        HTTPException: If email already exists.
    """
    # Check if user already exists
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Create new user
    user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Generate token
    access_token = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> TokenResponse:
    """Authenticate user and return JWT token.

    Args:
        credentials: User login credentials (email, password).
        session: Database session.

    Returns:
        JWT token and user info.

    Raises:
        HTTPException: If credentials are invalid.
    """
    # Find user by email
    result = await session.execute(
        select(User).where(User.email == credentials.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Generate token
    access_token = create_access_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get current authenticated user info.

    Args:
        current_user: Current authenticated user.

    Returns:
        User info.
    """
    return UserResponse.model_validate(current_user)
