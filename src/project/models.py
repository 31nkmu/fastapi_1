from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey

from auth.models import user
from sqlalchemy_imageattach.entity import Image

metadata = MetaData()
project = Table(
    'project',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('description', String, nullable=True),
    Column('owner_id', Integer, ForeignKey(user.c.id)),
)