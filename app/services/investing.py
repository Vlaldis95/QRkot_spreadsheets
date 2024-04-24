from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


def close_investing(objs: List[Base]) -> None:
    """Закрытие проектов или пожертвований"""
    for obj in objs:
        obj.fully_invested = (obj.full_amount == obj.invested_amount)
        if obj.fully_invested:
            obj.close_date = datetime.now()


async def investing_process(
    from_obj: Base,
    in_obj: Base,
    session: AsyncSession
) -> None:
    """Процесс «инвестирования»"""

    investments = await in_obj.get_not_fully_invested(session)
    for invest in investments:
        need_for_invest = from_obj.full_amount - from_obj.invested_amount
        free_for_invest = invest.full_amount - invest.invested_amount
        investing_amount = min(need_for_invest, free_for_invest)
        invest.invested_amount += investing_amount
        from_obj.invested_amount += investing_amount
        close_investing((invest, from_obj))
    await session.commit()