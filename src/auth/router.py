from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import get_async_session
from starlette.responses import JSONResponse

from project.models import Project
from .models import User
from .schemas import UserRead, UserCreate, UserOptional
from image.utils import get_full_link
from config import logger

router = APIRouter()


@router.get('/')
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    logger.info('get all users')
    try:
        query = select(User).options(selectinload(User.projects)).options(selectinload(User.images))
        result = await session.scalars(query)
        users = result.all()
        json_data = jsonable_encoder(users)
        for ind in range(len(users)):
            user = users[ind]
            json_data[ind].update({
                'project_count': user.project_count,
                'image_count': user.image_count,
            })
            json_data[ind].pop('images')
            json_data[ind].pop('projects')
        return JSONResponse(content=json_data)
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.get('/{user_id}', response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    logger.info('get one user')
    try:
        query = select(User).where(User.id == user_id).options(selectinload(User.projects).selectinload(Project.images))
        user = await session.scalar(query)
        json_data = jsonable_encoder(user)
        for project_data in json_data['projects']:
            get_full_link(project_data['images'])
        return JSONResponse(content=json_data)
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.delete('/{user_id}')
async def del_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    logger.info('delete one user')
    try:
        stmt = delete(User).where(User.id == user_id)
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'пользователь удален'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.put('/{user_id}')
async def put_user(user_id: int, new_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    logger.info('put user')
    try:
        stmt = update(User).where(User.id == user_id).values(**new_data.dict())
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'пользователь полностью изменен'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.patch('/{user_id}')
async def patch_project(user_id: int, new_data: UserOptional, session: AsyncSession = Depends(get_async_session)):
    logger.info('path user')
    try:
        new_data = {k: v for k, v in new_data.dict().items() if v}
        stmt = update(User).where(User.id == user_id).values(**new_data)
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'пользователь частично изменен'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)
