from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Получает список всех пожертвований."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date'
    },
)
async def get_user_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Получить список моих пожертвований."""
    return await donation_crud.get_by_user(session, user)


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude={
        'user_id',
        'invested_amount',
        'fully_invested',
        'close_date',
    },
    response_model_exclude_none=True
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),
):
    """Сделать пожертвование."""
    create_donation = await donation_crud.create(donation, session, user)
    await investing_process(
        from_obj=create_donation,
        in_obj=charity_project_crud,
        session=session
    )
    await session.refresh(create_donation)
    return create_donation