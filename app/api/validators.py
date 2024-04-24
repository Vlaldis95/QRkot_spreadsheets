from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_project_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    """Проверка на дубликат названия проекта"""
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_invested_amount(
        project_id: int,
        session: AsyncSession,
) -> None:
    """Проверяем, есть ли инвестиции в проекте."""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_project_exists_and_or_closed(
        project_id: int,
        session: AsyncSession,
        deletion: bool = False
) -> CharityProject:
    """Проверка на наличие самого проекта в БД"""
    charity_project = await charity_project_crud.get(project_id, session)
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    if charity_project.fully_invested:
        message = 'Закрытый проект нельзя редактировать!'
        if deletion:
            message = 'В проект были внесены средства, не подлежит удалению!'
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=message
        )
    return charity_project


async def check_project_full_amount(
        project_id: int,
        new_full_amount: int,
        session: AsyncSession,
) -> CharityProject:
    """Проверка требуемой суммы проекта"""
    charity_project = await charity_project_crud.get(project_id, session)
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Cумма не может быть меньше уже внесенной суммы!'
        )
    return charity_project