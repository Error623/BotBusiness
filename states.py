from aiogram.fsm.state import State, StatesGroup

class Leadform(StatesGroup):
    sphere = State() # Сфера
    problem = State() # Проблема
    volume = State() # Кол-во заявок в неделю
    priority = State() # Что важнее
    format = State() # Формат решения
    contact = State() # Контакты