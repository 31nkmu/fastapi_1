from typing import Optional, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean
from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base

from database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user_account'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    username: Mapped[str] = mapped_column(String(320), nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    projects: Mapped[List['Project']] = relationship(back_populates='user', cascade='all, delete-orphan')
    images: Mapped[List['Image']] = relationship(back_populates='user', cascade='all, delete-orphan')

    @property
    def project_count(self):
        return len(self.projects)

    @property
    def image_count(self):
        return len(self.images)
