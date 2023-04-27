from typing import Optional, List

from sqlalchemy import String, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from database import Base


class Project(Base):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('user_account.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship(back_populates='projects', passive_deletes=True, passive_updates=True)

    images: Mapped[List['Image']] = relationship(back_populates='project', cascade='all, delete-orphan')
