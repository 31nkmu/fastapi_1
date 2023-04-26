from fastapi import APIRouter, Depends, encoders, HTTPException
from pydantic.types import List
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from .models import project

from .schemas import ProjectCreate, ProjectOptional, ProjectRead

router = APIRouter(
    prefix='/projects',
    tags=['project']
)


@router.get('/', response_model=List[ProjectRead])
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(project)
        result = await session.execute(query)
        return result.all()
    except Exception:
        raise HTTPException(status_code=500)


@router.post('/')
async def add_project(new_project: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(project).values(**new_project.dict())
        await session.execute(stmt)
        await session.commit()
        return {'status': 'ok'}
    except Exception:
        raise HTTPException(status_code=500)


@router.patch('/{project_id}')
async def patch_project(project_id: int, new_data: ProjectOptional, session: AsyncSession = Depends(get_async_session)):
    try:
        new_data = {k: v for k, v in new_data.dict().items() if v}
        stmt = update(project).where(project.c.id == project_id).values(**new_data)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'ok'}
    except Exception:
        raise HTTPException(status_code=500)


@router.put('/{project_id}')
async def put_project(project_id: int, new_data: ProjectCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(project).where(project.c.id == project_id).values(**new_data.dict())
        await session.execute(stmt)
        await session.commit()
        return {'status': 'ok'}
    except Exception:
        raise HTTPException(status_code=500)


@router.delete('/{project_id}')
async def put_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(project).where(project.c.id == project_id)
        await session.execute(stmt)
        await session.commit()
        return {'status': 'ok'}
    except Exception:
        raise HTTPException(status_code=500)


@router.get('/{project_id}', response_model=ProjectRead)
async def get_one_project(project_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(project).where(project.c.id == project_id)
        result = await session.execute(query)
        return result.first()
    except Exception:
        raise HTTPException(status_code=500)
