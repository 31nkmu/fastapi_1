from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from starlette.responses import FileResponse

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.models import User
from auth.schemas import UserRead, UserCreate
from project.router import router as project_router
from image.router import router as image_router
from auth.router import router as user_router

from redis import asyncio as aioredis

app = FastAPI(
    title='Projects'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    user_router,
    prefix='/users',
    tags=['auth']
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


app.include_router(
    project_router
)

app.include_router(
    image_router
)


@app.get('/media/{img_path}', response_class=FileResponse, tags=['media'])
async def get_image(img_path: str):
    return f'media/{img_path}'


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
