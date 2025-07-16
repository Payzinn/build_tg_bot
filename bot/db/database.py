from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker 
from sqlalchemy.future import select
from sqlalchemy import or_, func, delete, update, case
from ..config import DATABASE_URL
from .models import *

engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def user_exists(user_tg_id: int):
    async with async_session() as session:  
        async with session.begin():
            result = await session.execute(select(User).where(User.user_tg_id == user_tg_id))
            user = result.scalar()
            return user is not None

async def get_user(user_tg_id: int):
    async with async_session() as session:  
        async with session.begin():
            result = await session.execute(select(User).where(User.user_tg_id == user_tg_id))
            user = result.scalar_one_or_none()
            return user


async def add_user(user_tg_id: int, user_tg_login: str):
    async with async_session() as session:
        new_user = User(
            user_tg_id = user_tg_id,
            user_tg_login = user_tg_login
        )
        session.add(new_user)
        await session.commit()

async def add_application(user_id: int, username_app: str, house_chosen: str, house_square:str, plot:str, budget:str, temp:str, comment:str, phone:str):
    async with async_session() as session:
        new_application = Application(
            user_id = user_id,
            username_app = username_app,
            house_chosen = house_chosen,
            house_square = house_square,
            plot = plot,
            budget = budget,
            temp = temp,
            comment = comment,
            phone = phone
        )
        session.add(new_application)
        await session.commit()
