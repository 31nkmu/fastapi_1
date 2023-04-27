from typing import Optional

from pydantic import BaseModel


class ImageRead(BaseModel):
    url: str
    user_id: int
    project_id: int

    class Config:
        orm_mode = True


