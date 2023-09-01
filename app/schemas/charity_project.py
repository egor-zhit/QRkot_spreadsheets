from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class ProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class ProjectCreate(ProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    @validator('name')
    def name_cant_be_null(cls, value):
        if value is None:
            raise ValueError('Название проекта не может быть пустым')
        return value

    @validator('description')
    def description_cant_be_null(cls, value):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым')
        return value

    @validator('full_amount')
    def full_amount_cant_be_null(cls, value):
        if value is None:
            raise ValueError('Требуемая сумма должна быть больше нуля')
        return value


class ProjectUpdate(ProjectBase):
    pass


class ProjectDB(ProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True