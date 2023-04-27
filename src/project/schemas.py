from typing import Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str]
    user_id: int


class ProjectRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    user_id: int

    class Config:
        orm_mode = True


class ProjectOptional(ProjectCreate):
    __annotations__ = {k: Optional[v] for k, v in ProjectCreate.__annotations__.items()}
