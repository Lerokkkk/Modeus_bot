from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, KeyboardBuilder, KeyboardButton



# TODO это с помощью билдера, есть еще статичные
def start_conversation():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Ввести данные от Modeus'),
                KeyboardButton(text='Ввести данные от Google Calendar'),
                KeyboardButton(text='Обновить пары'))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Выбери')


# Статичные но уже инлайн
def get_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="❌Отменить ввод данных❌", callback_data="cancel"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
