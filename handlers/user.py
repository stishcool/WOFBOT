from aiogram import types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot import dp, db, bot
from utils.check_subscription import check_subscriptions
from utils.referral import generate_referral_link
from utils.game_logic import choose_game  # Импортируем функцию choose_game
from config import ADMIN_ID

# Команда /start
@dp.message_handler(CommandStart())
async def send_welcome(message: types.Message):
    referrer_id = None
    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    # Проверяем, есть ли пользователь в базе
    user = db.get_user(user_id)
    if not user:
        # Если есть реферер
        if args:
            referrer_id = int(args)
            # Начисляем поинт рефереру
            db.add_ticket(referrer_id)
        # Добавляем пользователя в базу
        db.add_user(user_id, username, full_name, referrer_id)
    
    # Отправляем приветствие и список каналов
    channels = db.get_channels()
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        button = InlineKeyboardButton(text=channel[1], url=channel[2])
        keyboard.add(button)
    # Добавляем кнопку "Проверить подписку"
    check_button = InlineKeyboardButton(text="Проверить подписку", callback_data="check_subscription")
    keyboard.add(check_button)

    await message.answer(f"Привет, {full_name}! Подпишись на каналы ниже:", reply_markup=keyboard)

# Обработчик проверки подписки
@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def process_subscription(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    channels = db.get_channels()
    is_subscribed = await check_subscriptions(user_id, channels, bot)
    
    if is_subscribed:
        db.update_subscription_status(user_id, 1)
        # Отправляем меню
        await bot.send_message(user_id, "Спасибо за подписку!", reply_markup=main_menu_keyboard())
    else:
        await bot.send_message(user_id, "Вы не подписались на все каналы.")

# Клавиатура главного меню
def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Играть", "Профиль")
    keyboard.add("Получить билеты", "Стать спонсором")
    return keyboard

# Обработчик текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if not user['subscribed'] and message.text != "Стать спонсором":
        await message.answer("Для начала подпишитесь на каналы.")
        return

    if message.text == "Играть":
        tickets = user['tickets']
        if tickets <= 0:
            await message.answer("У вас нет билетов.")
            return
        # Списываем билет
        db.add_ticket(user_id, -1)
        # Получаем список игр и их вероятности
        games = db.get_games()
        # Реализуем выбор игры на основе вероятности
        game = choose_game(games, user_id)
        await message.answer(f"Результат игры: {game['game_text']}")
    elif message.text == "Профиль":
        tickets = user['tickets']
        await message.answer(f"У вас {tickets} билетов.")
    elif message.text == "Получить билеты":
        referral_link = generate_referral_link(user_id)
        await message.answer(f"Ваша реферальная ссылка: {referral_link}")
    elif message.text == "Стать спонсором":
        await message.answer("Стать спонсором")
    else:
        await message.answer("Неизвестная команда.")
