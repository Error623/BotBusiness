import os 
import logging 
import asyncio 
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types, Router
from aiogram.types import Message, CallbackQuery
from aiogram import BaseMiddleware
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext 
from keyboards import main_menu, chaos, appoitments, important, format, contacts
from states import Leadform
from db import create_tables, save_form

# Логирование действий и создание конфинга для записей логов
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message):
            logger.info(
                f"MESSAGE | user_id={event.from_user.id} | text={event.text}"
            )
        return await handler(event, data)

class CallbackLoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, CallbackQuery):
            logger.info(
                f"CALLBACK | user_id={event.from_user.id} | data={event.data}"
            )
        return await handler(event, data)

# ENV
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split(",")))

# Bot
bot = Bot(token=BOT_TOKEN) 
dp = Dispatcher(storage=MemoryStorage()) 

router = Router()
dp.include_router(router)

dp.message.middleware(LoggingMiddleware())
dp.callback_query.middleware(CallbackLoggingMiddleware()) 

# Handlers
@router.message(CommandStart())
async def start(message: types.Message):
    await message.answer("""
        Привет! 👋\n
        Я бот команды «Автоматизация | Business».\n 
        За 1 минуту уточню пару вопросов и передам менеджеру, чтобы он предложил решение
под ваш бизнес.\n 
                                                                                 
""")
    await message.answer(
        "Начнём?",
     reply_markup=main_menu() 
    )

@router.callback_query(F.data == "yes")
async def ask_sphere(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Напишите в какой сфере ваш бизнес?"
    )
    await state.set_state(Leadform.sphere)
    await callback.answer()

@router.callback_query(F.data == "later")
async def later(callback: types.CallbackQuery):
    await callback.message.answer(
        "Хорошо, обращайтесь позже!"
    )
    await callback.answer()

@router.message(Leadform.sphere)
async def get_sphere(message: Message, state: FSMContext):
    await state.update_data(sphere=message.text)

    await message.answer(
        "Где сейчас больше всего рутины или хаоса?",
        reply_markup=chaos()
    )
    await state.set_state(Leadform.problem)

@router.callback_query(Leadform.problem)
async def get_problem(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(problem=callback.data) 

    await callback.message.answer(
        "Сколько примерно обращений или заявок у вас в неделю?",
        reply_markup=appoitments()
    )
    await state.set_state(Leadform.volume)
    await callback.answer()

@router.message(Leadform.problem)
async def get_problem_text(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await message.answer(
        "Сколько примерно обращений или заявок у вас в неделю?",
        reply_markup=appoitments()
    )
    await state.set_state(Leadform.volume)

@router.callback_query(Leadform.volume)
async def step_priority(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(volume=callback.data)

    await callback.message.answer(
        "Что для вас сейчас важнее всего?",
        reply_markup=important()
    )
    await state.set_state(Leadform.priority)
    await callback.answer()

@router.callback_query(Leadform.priority)
async def step_format(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(priority=callback.data)

    await callback.message.answer(
        "Какой формат решения вам ближе?",
        reply_markup=format()
    )
    await state.set_state(Leadform.format)
    await callback.answer()

@router.callback_query(Leadform.format)
async def step_contact(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(format=callback.data)

    await callback.message.answer(
        "Оставьте номер телефона, менеджер свяжется с вами и предложит решение",
        reply_markup=contacts()
    )
    await state.set_state(Leadform.contact)
    await callback.answer()

@router.message(Leadform.contact, F.contact)
async def finish_contact(message: Message, state: FSMContext):
    """Обработка кнопки 'Поделиться номером'"""
    await state.update_data(contact=message.contact.phone_number)
    
    data = await state.get_data()
    save_form(data, message.from_user.id)

    text = f"""
Новая заявка 🔥

Ниша: {data['sphere']}
Боль: {data['problem']}
Поток: {data['volume']}
Цель: {data['priority']}
Формат: {data['format']}
Телефон: {data['contact']}
TG: @{message.from_user.username or '-'}
    """
    
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logger.error(f"Failed to send to admin {admin_id}: {e}")
    
    await message.answer(
        "Спасибо! Заявка принята ✅\n"
        "Менеджер свяжется с вами в течение дня\n"
        "Пока можете посмотреть примеры работ и кейсы в нашем канале"
    )
    await state.clear()

@router.message(Leadform.contact)
async def finish_text(message: Message, state: FSMContext):
    """Обработка ручного ввода номера"""
    await state.update_data(contact=message.text)
    
    data = await state.get_data()
    save_form(data, message.from_user.id)

    text = f"""
Новая заявка 🔥

Ниша: {data['sphere']}
Боль: {data['problem']}
Поток: {data['volume']}
Цель: {data['priority']}
Формат: {data['format']}
Телефон: {data['contact']}
TG: @{message.from_user.username or '-'}
    """
    
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            logger.error(f"Failed to send to admin {admin_id}: {e}")
    
    await message.answer(
        "Спасибо! Заявка принята ✅\n"
        "Менеджер свяжется с вами в течение дня\n"
        "Пока можете посмотреть примеры работ и кейсы в нашем канале"
    )
    await state.clear()

async def main():
    create_tables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())