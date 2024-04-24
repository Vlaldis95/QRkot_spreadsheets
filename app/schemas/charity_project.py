from datetime import datetime
from typing import Optional

from pydantic import (BaseModel, Extra, Field, PositiveInt, root_validator,
                      validator)

from .constants import CHARITY_MAX, CHARITY_MIN


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=CHARITY_MIN, max_length=CHARITY_MAX)
    description: Optional[str] = Field(None, min_length=CHARITY_MIN)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., min_length=CHARITY_MIN, max_length=CHARITY_MAX,
        title='Название проекта',
        description='Укажите название благотворительного проекта'
    )
    description: str = Field(
        ..., min_length=CHARITY_MIN,
        title='Описание проекта',
        description='Укажите описание к проекту'
    )
    full_amount: PositiveInt = Field(
        ...,
        title='Требуемая сумма',
        description='Укажите какая сумма нужна на проект'
    )

    class Config:
        @validator('name')
        def max_length(cls, value: str):
            if len(value) > CHARITY_MAX:
                raise ValueError('Название не должно превышать 100 символов')
            if value.isnumeric():
                raise ValueError('Название не может быть числом')
            return value

        @root_validator(skip_on_failure=True)
        def check_empty(cls, values):
            if values is None:
                raise ValueError('Поле не может быть нулевым или пустым')
            return values


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True