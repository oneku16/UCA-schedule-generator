from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.services import ScheduleService
from src.infrastructure.orm import SQLScheduleRepository
from src.infrastructure.database import get_db
from src.schemas import APIResponse, ScheduleResponse, ScheduleUpdate
from schedule import build


router = APIRouter()


@router.get(path='/generate/')
async def generate_schedule_and_save(owner_id: int, schedule_name: str, db: AsyncSession = Depends(get_db)):
    schedule_service = ScheduleService(SQLScheduleRepository(db))
    existing_schedule = await schedule_service.get_schedule_by_name(schedule_name=schedule_name)
    if existing_schedule:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Schedule already exists",
        )
    try:
        schedule_generated = await run_in_threadpool(build)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating schedule: {e}",
        )

    schedule_data = {
        "schedule_name": schedule_name,
        "data": schedule_generated,
        "owner_id": owner_id,
    }

    schedule = await schedule_service.create_schedule(schedule_data)

    return APIResponse(
        message="Schedule generated successfully.",
        data=ScheduleResponse.model_validate(schedule)
    )


@router.put(path="/update/", response_model=APIResponse, tags=["Schedule"])
async def update_schedule(schedule_data: ScheduleUpdate, db: AsyncSession = Depends(get_db)):
    schedule_service = ScheduleService(SQLScheduleRepository(db))
    updated = await schedule_service.update_schedule(schedule_data.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return APIResponse(
        message="Schedule updated successfully",
        data=ScheduleResponse.model_validate(updated)
    )


@router.delete(path="/{schedule_id}/delete", response_model=APIResponse, tags=["Schedule"])
async def delete_schedule(schedule_id: int, db: AsyncSession = Depends(get_db)):
    schedule_service = ScheduleService(SQLScheduleRepository(db))
    deleted = await schedule_service.delete_schedule(schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return APIResponse(
        message="Schedule deleted successfully",
        data={"schedule_id": schedule_id},
    )


@router.get(path='/get/', response_model=APIResponse, tags=["Schedule"])
async def get_schedule(
        schedule_id: Optional[int] = None,
        schedule_name: Optional[str] = None,
        db: AsyncSession = Depends(get_db),
):
    schedule_service = ScheduleService(SQLScheduleRepository(db))

    if schedule_id is not None:
        schedule = await schedule_service.get_schedule_by_id(schedule_id=schedule_id)
    elif schedule_name is not None:
        schedule = await schedule_service.get_schedule_by_name(schedule_name=schedule_name)
    else:
        raise HTTPException(status_code=400, detail="schedule_id or schedule_name must be provided")

    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return APIResponse(
        message="Schedule retrieved successfully",
        data=ScheduleResponse.model_validate(schedule)
    )
