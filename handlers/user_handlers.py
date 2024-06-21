import os

from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup, default_state
from db.db_connect import *
from keyboards.keyboard import get_keyboard
from services.modeus_parser import Parser
from services.google_calendar import GoogleCalendar
from keyboards import keyboard

import aiofiles.os

router = Router()


class FSMModeusState(StatesGroup):
    pending_credentials = State()
    received_credentials = State()


class FSMGoogleState(StatesGroup):
    pending_credentials = State()
    received_credentials = State()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await add_user_id_in_user_db(str(message.from_user.id))
    if not await aiofiles.os.path.exists(os.path.join('./users_data/', str(message.from_user.id))):
        await aiofiles.os.makedirs(os.path.join('./users_data/', str(message.from_user.id)))
        await aiofiles.os.makedirs(os.path.join('./users_data/', str(message.from_user.id), 'modeus_calendar'))
        await aiofiles.os.makedirs(os.path.join('./users_data/', str(message.from_user.id), 'json_calendar'))

    await message.answer(text=f'{message.from_user.id} - Здарова!\n'
                              'Добавь ссылку у себя в гугл календаре! - '
                              '<u>https://calendar.google.com/calendar/u/0/r/settings</u>\n'
                              'Копировать:\n <code>fuckuuu@optimum-spring-405211.iam.gserviceaccount.com</code>',
                         reply_markup=keyboard.start_conversation())


# update events
@router.message(F.text == 'Обновить пары')
async def process_update_events(message: Message):
    calendar_data: CalendarData = await check_user_id_in_db(CalendarData, str(message.from_user.id))
    modeus_data: ModeusData = await check_user_id_in_db(ModeusData, str(message.from_user.id))
    if calendar_data is None:
        await message.answer('Calendar id empty')
        return
    elif modeus_data is None:
        await message.answer("Modeus data empty")
        return
    login = modeus_data.login
    password = modeus_data.password
    calendar_id = calendar_data.calendar_id
    google_object = GoogleCalendar(dir=message.from_user.id,
                                   calendar_id=calendar_id)
    modeus_object = Parser(dir=message.from_user.id, user_login=login, user_password=password)
    data = await google_object.find_max_and_min_time()
    print(f'Data is {data}')
    if data is None:
        await modeus_object.get_data_selen()
        flag = await modeus_object.parsing_file()
        if flag is False:
            await message.answer('Расписания пока что нет')
            return
        await google_object.add_events()
    else:
        time_min, time_max = data
        await google_object.delete_events(time_min, time_max)
        await modeus_object.get_data_selen()
        await modeus_object.parsing_file()
        await google_object.add_events()


@router.message(F.text.startswith('Ввести данные от Google Calendar'))
async def pending_modeus_credentials(message: Message, state: FSMContext):
    await message.answer('Введите пожалуйста calendar id', reply_markup=get_keyboard())
    await state.set_state(FSMGoogleState.pending_credentials)


@router.message(FSMGoogleState.pending_credentials)
async def process_add_calendar_id(message: Message, state: FSMContext):
    args = message.text.split()
    await message.answer(f'{args}')
    if len(args) != 1:
        await message.answer(f'{args}: {len(args)}')
        return await message.answer('Нужен 1 аргумент')
    await add_calendar_id_in_calendar_data_db(user_id=str(message.from_user.id), calendar_id=message.text)
    await message.answer(f'Done✅')
    await state.clear()


@router.message(F.text.startswith('Ввести данные от Modeus'))
async def receiving_modeus_credentials(message: Message, state: FSMContext):
    await message.answer('Введите пожалуйста данные в формате login password через пробел.',
                         reply_markup=get_keyboard())
    await state.set_state(FSMModeusState.pending_credentials)


@router.message(FSMModeusState.pending_credentials)
async def process_add_modeus_data(message: Message, state: FSMContext):
    args = message.text.split()
    if len(args) != 2:
        return message.answer(f'Нужно 2 аргумента, вы ввели {len(args)}')

    login, password = args[-2], args[-1]
    await add_modeus_data_in_modeus_db(user_id=str(message.from_user.id), login=login, password=password)
    await message.answer('Done✅')
    await state.clear()


@router.callback_query(F.data.startswith('cancel'))
async def cancel_input_credetials(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Отменили ввод данных✅')
    await state.clear()


@router.message()
async def empty_message(message: types.Message, state: FSMContext):
    await message.answer('Такой команды не знаем', reply_markup=keyboard.start_conversation())
