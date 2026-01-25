from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data="yes")],
            [InlineKeyboardButton(text="⏳ Позже", callback_data="later")]
        ]
    )



def chaos():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Заявки в личке / мессенджерах", callback_data="problem_dm")],
            [InlineKeyboardButton(text="Долго отвечаем клиентам", callback_data="deploy_clients")],
            [InlineKeyboardButton(text="Теряются заявки", callback_data="no_appoitments")],
            [InlineKeyboardButton(text="Запись / расписание / напоминания", callback_data="problem_schedule")],
            [InlineKeyboardButton(text="Нет учёта клиентов", callback_data="no_clients")],
            [InlineKeyboardButton(text="Другое (ввод текста)", callback_data="or_something")],
        ]
    )



def appoitments():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="0-10", callback_data="10")],
            [InlineKeyboardButton(text="10-30", callback_data="30")],
            [InlineKeyboardButton(text="30-100", callback_data="100")],
            [InlineKeyboardButton(text="100+", callback_data="more")]
        ]
    )



def important():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Экономия времени владельца", callback_data="economy")],
            [InlineKeyboardButton(text="Увеличение продаж", callback_data="more_orders")],
            [InlineKeyboardButton(text="Навести порядок и контроль", callback_data="control")],
            [InlineKeyboardButton(text="Ускорить обработку клиентов", callback_data="proccessing")],
            [InlineKeyboardButton(text="Снизить нагрузку на сотрудников", callback_data="load")]
        ]
    )



def format():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Быстро закрыть одну задачу", callback_data="fast_close")],
            [InlineKeyboardButton(text="Сделать систему под ключ", callback_data="system")],
            [InlineKeyboardButton(text="Максимально автоматизировать бизнес", callback_data="max")],
            [InlineKeyboardButton(text="Пока не понимаю, нужна консультация", callback_data="consultation")],
        ]
    )



def contacts():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Отправить контакт", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard = True
    )