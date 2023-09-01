from sqlalchemy import select
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.crud.base import CRUDBase


class CRUDProject(CRUDBase):

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_amount(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> int:
        db_amount = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == project_id
            )
        )
        db_amount = db_amount.scalars().first()
        return db_amount

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:

        projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            )
        )

        projects = projects.scalars().all()
        projects.sort(
            key=lambda project: project.close_date - project.create_date
        )
        return projects


project_crud = CRUDProject(CharityProject)
