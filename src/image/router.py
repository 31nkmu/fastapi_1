import os
import shutil
from typing import List

from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .utils import get_full_link, del_file

from database import get_async_session

from .models import Image
from .schemas import ImageRead

from config import logger

router = APIRouter(
    prefix='/images',
    tags=['image']
)


@router.post('/')
async def add_image(user_id: int, project_id: int, file: UploadFile,
                    session: AsyncSession = Depends(get_async_session)):
    logger.info('create image')
    try:
        if not os.path.exists('media'):
            os.mkdir('media')
        with open('media/' + file.filename, 'wb') as image:
            shutil.copyfileobj(file.file, image)

        url = str(f'media/{file.filename}')
        stmt = insert(Image).values(
            url=url,
            project_id=project_id,
            user_id=user_id
        )
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'картинка добавлена'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.get('/', response_model=List[ImageRead])
async def read_image(session: AsyncSession = Depends(get_async_session)):
    logger.info('get all images')
    try:
        query = select(Image)
        result = await session.scalars(query)
        json_data = jsonable_encoder(result.all())
        json_data = get_full_link(json_data)
        return JSONResponse(content=json_data)
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.delete('/{image_id}')
async def del_image(image_id: int, session: AsyncSession = Depends(get_async_session)):
    logger.info('delete image')
    try:
        await del_file(image_id, session)
        query = select(Image).where(Image.id == image_id)
        await session.scalar(query)
        stmt = delete(Image).where(Image.id == image_id)
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'картинка удалена'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)
