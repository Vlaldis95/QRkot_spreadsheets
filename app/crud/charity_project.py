from typing import List, Optional

from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        """Запрос проекта по номеру id"""

        project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return project_id.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        """Запрос на все завершённые проекты."""

        projects = await session.execute(
            select([CharityProject.name,
                    CharityProject.description,
                    CharityProject.create_date,
                    CharityProject.close_date]).where(
                CharityProject.fully_invested.is_(True)
            ).order_by(
                extract(CharityProject.close_date - CharityProject.create_date))
        )
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)