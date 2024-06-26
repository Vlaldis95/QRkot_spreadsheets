from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_project_exists_and_or_closed,
                                check_project_full_amount,
                                check_project_invested_amount,
                                check_project_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import investing_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    await check_project_name_duplicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investing_process(
        from_obj=new_project,
        in_obj=donation_crud,
        session=session
    )
    await session.refresh(new_project)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    upd_charity_project = await check_project_exists_and_or_closed(
        project_id, session
    )
    if obj_in.name is not None:
        await check_project_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        upd_charity_project = await check_project_full_amount(
            project_id,
            obj_in.full_amount,
            session
        )
    upd_charity_project = await charity_project_crud.update(
        upd_charity_project, obj_in, session
    )
    await investing_process(
        from_obj=upd_charity_project,
        in_obj=donation_crud,
        session=session
    )
    await session.refresh(upd_charity_project)
    return upd_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    rm_charity_project = await check_project_exists_and_or_closed(
        project_id, session, True
    )
    await check_project_invested_amount(project_id, session)
    return await charity_project_crud.remove(
        rm_charity_project, session
    )