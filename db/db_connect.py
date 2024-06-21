import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .models import User, ModeusData, CalendarData, Base
from config.config import DATABASE_URL


async def add_user_id_in_user_db(user_id):
    async with async_session() as session:
        if await check_user_id_in_db(User, user_id) is None:
            session.add(User(user_id=user_id))
            await session.commit()


async def add_calendar_id_in_calendar_data_db(user_id, calendar_id):
    async with async_session() as session:
        if await check_user_id_in_db(CalendarData, user_id) is None:
            session.add(CalendarData(user_id=user_id, calendar_id=calendar_id))
            await session.commit()
            return f'Добавили calendar_id для {user_id}'
        else:
            query = select(CalendarData).filter(CalendarData.user_id == user_id)
            user_data = await session.execute(query)
            user_data.scalar_one().calendar_id = calendar_id
            await session.commit()
            return f'Изменили calendar_id для {user_id}'


async def add_modeus_data_in_modeus_db(user_id, login, password):
    async with async_session() as session:
        if await check_user_id_in_db(ModeusData, user_id) is None:
            session.add(ModeusData(user_id=user_id, login=login, password=password))
            await session.commit()
            return f'Добавили login, password для {user_id}'
        else:
            query = select(ModeusData).filter(ModeusData.user_id == user_id)
            user_result = await session.execute(query)
            user_obj = user_result.scalar_one()  # Получаем один объект из результата запроса
            user_obj.login = login
            user_obj.password = password
            await session.commit()
            return f'Изменили login, password для {user_id}'


async def check_user_id_in_db(db_name, user_id):
    async with async_session() as session:
        query = select(db_name).filter(db_name.user_id == user_id)
        res = await session.execute(query)

        return res.scalar()


# Создаем соединение с базой данных
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)