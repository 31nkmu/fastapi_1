from fastapi import APIRouter, Depends, encoders, HTTPException
from pydantic.types import List
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .models import Project

from .schemas import ProjectCreate, ProjectOptional, ProjectRead
from config import logger

router = APIRouter(
    prefix='/projects',
    tags=['project']
)


@router.get('/', response_model=List[ProjectRead])
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    logger.info('get all projects')
    try:
        query = select(Project)
        result = await session.scalars(query)
        return result.all()
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.post('/')
async def add_project(new_project: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    logger.info('create project')
    try:
        stmt = insert(Project).values(**new_project.dict())
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'проект успешно создан'}
    except IntegrityError as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=400, detail='Нет такого пользователя')
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.patch('/{project_id}')
async def patch_project(project_id: int, new_data: ProjectOptional, session: AsyncSession = Depends(get_async_session)):
    logger.info('patch project')
    try:
        new_data = {k: v for k, v in new_data.dict().items() if v}
        stmt = update(Project).where(Project.id == project_id).values(**new_data)
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'проект частично изменен'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.put('/{project_id}')
async def put_project(project_id: int, new_data: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    logger.info('put project')
    try:
        stmt = update(Project).where(Project.id == project_id).values(**new_data.dict())
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'проект полностью изменен'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.delete('/{project_id}')
async def put_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    logger.info('delete project')
    try:
        stmt = delete(Project).where(Project.id == project_id)
        await session.execute(stmt)
        await session.commit()
        return {'msg': 'проект успешно удален'}
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)


@router.get('/{project_id}', response_model=ProjectRead)
async def get_one_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    logger.info('get one project')
    try:
        query = select(Project).where(Project.id == project_id)
        result = await session.scalar(query)
        return result
    except Exception as ex_:
        logger.info(ex_)
        raise HTTPException(status_code=500)
