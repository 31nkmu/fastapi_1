import os

from core.config import HOST, PORT
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from .models import Image


def get_full_link(json_data):
    for dict_ in json_data:
        dict_['url'] = f"http://{HOST}:{PORT}/{dict_['url']}"
    return json_data


async def del_file(file_id, session):
    query = select(Image).where(Image.id == file_id)
    result = await session.scalar(query)
    json_data = jsonable_encoder(result)
    file_path = json_data['url']
    # file_name = file_path.split('/')[-1]
    if os.path.isfile(file_path):
        os.remove(file_path)
