from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.services import UserService
from src.infrastructure.orm import SQLUserRepository
from src.infrastructure.database import get_db
from src.schemas import APIResponse, UserCreate, UserResponse


router = APIRouter()


@router.post("/create/", response_model=APIResponse, tags=["Users"])
async def user_create(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(SQLUserRepository(db))
    existing_user = await user_service.is_user_exists(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    new_user = await user_service.create_user(user_data=user_data)

    return APIResponse(
        message="User created successfully.",
        data=UserResponse.model_validate(new_user)
    )