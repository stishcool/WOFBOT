from aiogram import types
from bot import dp, bot
from config import ADMIN_ID

# Хендлеры для админа
@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("У вас нет доступа к этой команде.")
        return
    # Отображаем админ-панель
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Добавить канал", "Удалить канал")
    keyboard.add("Добавить игру", "Удалить игру")
    keyboard.add("Список пользователей")
    await message.answer("Админ-панель", reply_markup=keyboard)

# Обработчики для админских функций
@dp.message_handler(lambda message: message.text == "Добавить канал" and message.from_user.id == ADMIN_ID)
async def add_channel(message: types.Message):
    await message.answer("Отправьте название канала и ссылку через запятую.")
    # Используй FSM (Finite State Machine) для дальнейшего ввода

