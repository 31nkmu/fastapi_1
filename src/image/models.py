from typing import Optional

from sqlalchemy import String, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from core.database import Base


class Image(Base):
    __tablename__ = 'image'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    url: Mapped[str] = mapped_column(URLType)

    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='images', passive_deletes=True, passive_updates=True)

    project_id: Mapped[int] = mapped_column(ForeignKey('project.id', ondelete='CASCADE'))
    project: Mapped['Project'] = relationship(back_populates='images', passive_deletes=True, passive_updates=True)
