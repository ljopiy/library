import sqlite3
import logging
from datetime import datetime, timezone, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
API_TOKEN = "8525429388:AAFGxB6UYgaFMlnSDEVOWXeLm8Xx8JCNRNI"
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# ID администратора
ADMIN_ID = 671470151

# Временная зона Екатеринбурга (UTC+5)
YEKATERINBURG_OFFSET = timezone(timedelta(hours=5))


def get_current_time():
    """Получение текущего времени в Екатеринбурге"""
    return datetime.now(YEKATERINBURG_OFFSET)


# Состояния для пользователей
class UserRegistration(StatesGroup):
    waiting_for_reader_ticket = State()
    confirming_reader_ticket = State()


# Состояния для админа
class AdminStates(StatesGroup):
    waiting_for_message_type = State()
    waiting_for_book_days = State()
    waiting_for_ticket_days = State()
    waiting_for_book_title = State()
    waiting_for_reader_ticket_for_book = State()
    waiting_for_reader_ticket_for_ticket = State()
    waiting_for_custom_message = State()
    waiting_for_reader_ticket_for_custom = State()


# Инициализация SQLite базы данных
def init_database():
    """Инициализация SQLite базы данных"""
    conn = sqlite3.connect('library_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS library_users (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            id_tg BIGINT UNIQUE NOT NULL,
            id_reader_ticket VARCHAR(50) UNIQUE,
            registered_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")


def get_db_connection():
    """Получение соединения с SQLite"""
    return sqlite3.connect('library_bot.db')


# Клавиатуры для пользователей
def get_confirmation_keyboard():
    """Клавиатура для подтверждения номера читательского билета"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("✅ Да, верно", callback_data="confirm_yes"),
        types.InlineKeyboardButton("❌ Нет, изменить", callback_data="confirm_no")
    )
    return keyboard


# Клавиатуры для админа
def get_admin_keyboard():
    """Клавиатура админ-панели"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("📚 Скоро будет просрочена сдача книги"),
        types.KeyboardButton("🎫 Скоро завершится действие читательского билета"),
        types.KeyboardButton("📢 Отправить иное уведомление")
    )
    return keyboard


def get_days_keyboard():
    """Клавиатура выбора дней"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton("1 день"),
        types.KeyboardButton("3 дня"),
        types.KeyboardButton("5 дней")
    )
    return keyboard


# Проверка прав администратора
def is_admin(user_id):
    return user_id == ADMIN_ID


# Обработчики команд для пользователей
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    # Проверяем, зарегистрирован ли пользователь
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM library_users WHERE id_tg = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            # Пользователь уже зарегистрирован
            registered_time = datetime.strptime(user[3], '%Y-%m-%d %H:%M:%S')
            formatted_time = registered_time.strftime('%d.%m.%Y в %H:%M')

            await message.answer(
                f"👋 С возвращением, {user_name}!\n"
                f"📚 Ваш читательский билет: <b>{user[2]}</b>\n"
                f"📅 Вы зарегистрированы: {formatted_time} (Екатеринбург)\n\n"
                f"📢 <i>Этот бот предназначен для уведомлений о:\n"
                f"• Сроке сдачи книг\n• Продлении читательского билета\n"
                f"• Важных библиотечных новостях</i>",
                parse_mode="HTML"
            )
        else:
            # Новый пользователь - начинаем регистрацию
            current_time = get_current_time().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                'INSERT INTO library_users (id_tg, registered_at) VALUES (?, ?)',
                (user_id, current_time)
            )
            conn.commit()

            welcome_text = (
                f"📚 Добро пожаловать в библиотечную систему, {user_name}!\n\n"
                f"<b>📢 О назначении бота:</b>\n"
                f"Этот бот создан для уведомления читателей о:\n"
                f"• ⏰ Скоро окончании срока сдачи книг\n"
                f"• 📅 Необходимости продления читательского билета\n"
                f"• 🔔 Важных библиотечных обновлениях\n\n"
                f"<i>❌ Бот НЕ используется для рекламных рассылок!</i>\n\n"
                f"Пожалуйста, введите номер вашего читательского билета:"
            )

            await message.answer(
                welcome_text,
                parse_mode="HTML",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await UserRegistration.waiting_for_reader_ticket.set()

    except Exception as e:
        logger.error(f"Error in /start: {e}")
        await message.answer("❌ Произошла ошибка. Пожалуйста, попробуйте позже.")
    finally:
        conn.close()


@dp.message_handler(state=UserRegistration.waiting_for_reader_ticket)
async def process_reader_ticket(message: types.Message, state: FSMContext):
    """Обработка введенного номера читательского билета"""
    reader_ticket = message.text.strip()

    # Проверяем валидность номера
    if not reader_ticket:
        await message.answer("❌ Пожалуйста, введите корректный номер читательского билета:")
        return

    if len(reader_ticket) > 50:
        await message.answer("❌ Номер билета слишком длинный. Максимум 50 символов:")
        return

    # Проверяем, не занят ли уже этот номер билета
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM library_users WHERE id_reader_ticket = ?', (reader_ticket,))
        existing_user = cursor.fetchone()

        if existing_user:
            await message.answer(
                "❌ Этот номер читательского билета уже зарегистрирован.\n"
                "Пожалуйста, введите другой номер:"
            )
            return

        # Сохраняем номер во временное хранилище
        await state.update_data(reader_ticket=reader_ticket)

        # Запрашиваем подтверждение
        confirmation_text = (
            f"📋 Проверьте правильность введенных данных:\n\n"
            f"📚 Номер читательского билета: <b>{reader_ticket}</b>\n\n"
            f"⚠️ <i>Внимание! Читательский билет привязывается навсегда и не может быть изменен!</i>\n\n"
            f"📢 <i>После регистрации вы будете получать уведомления о:\n"
            f"• Сроке сдачи книг\n• Продлении читательского билета\n"
            f"• Библиотечных новостях</i>\n\n"
            f"Всё верно?"
        )

        await message.answer(
            confirmation_text,
            parse_mode="HTML",
            reply_markup=get_confirmation_keyboard()
        )

        await UserRegistration.confirming_reader_ticket.set()

    except Exception as e:
        logger.error(f"Error processing reader ticket: {e}")
        await message.answer("❌ Произошла ошибка. Пожалуйста, попробуйте позже.")
    finally:
        conn.close()


@dp.callback_query_handler(lambda c: c.data in ['confirm_yes', 'confirm_no'],
                           state=UserRegistration.confirming_reader_ticket)
async def process_confirmation(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка подтверждения номера читательского билета"""
    user_id = callback_query.from_user.id

    # Удаляем сообщение с инлайн-кнопками
    try:
        await bot.delete_message(chat_id=user_id, message_id=callback_query.message.message_id)
    except Exception as e:
        logger.error(f"Error deleting message: {e}")

    if callback_query.data == 'confirm_yes':
        # Подтверждение - сохраняем номер билета
        user_data = await state.get_data()
        reader_ticket = user_data.get('reader_ticket')

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE library_users SET id_reader_ticket = ? WHERE id_tg = ?',
                (reader_ticket, user_id)
            )
            conn.commit()

            # Получаем время регистрации для финального сообщения
            cursor.execute('SELECT registered_at FROM library_users WHERE id_tg = ?', (user_id,))
            registered_time = cursor.fetchone()[0]
            formatted_time = datetime.strptime(registered_time, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y в %H:%M')

            success_text = (
                f"✅ Регистрация завершена успешно!\n\n"
                f"📚 Ваш читательский билет: <b>{reader_ticket}</b>\n"
                f"📅 Дата регистрации: {formatted_time} (Екатеринбург)\n\n"
                f"🔒 <i>Читательский билет привязан к вашему аккаунту навсегда.</i>\n\n"
                f"📢 <b>Теперь вы будете получать уведомления:</b>\n"
                f"• ⏰ О скором окончании срока сдачи книг\n"
                f"• 📅 О необходимости продления читательского билета\n"
                f"• 🔔 О важных библиотечных обновлениях\n\n"
                f"<i>❌ Рекламные рассылки не производятся!</i>"
            )

            await bot.send_message(
                user_id,
                success_text,
                parse_mode="HTML"
            )

        except Exception as e:
            logger.error(f"Error confirming reader ticket: {e}")
            await bot.send_message(user_id, "❌ Произошла ошибка при сохранении данных.")
        finally:
            conn.close()

        await state.finish()

    else:
        # Отмена - запрашиваем номер заново
        await bot.send_message(
            user_id,
            "🔄 Пожалуйста, введите номер читательского билета заново:"
        )
        await UserRegistration.waiting_for_reader_ticket.set()

    await bot.answer_callback_query(callback_query.id)


# Обработчики команд для админа
@dp.message_handler(commands=['message'])
async def cmd_message(message: types.Message):
    """Обработчик команды /message для админа"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав для использования этой команды.")
        return

    await message.answer(
        "👨‍💼 Админ-панель уведомлений\n\n"
        "Выберите тип уведомления:",
        reply_markup=get_admin_keyboard()
    )
    await AdminStates.waiting_for_message_type.set()


# Обработчики для админ-панели
@dp.message_handler(lambda message: message.text == "📚 Скоро будет просрочена сдача книги",
                    state=AdminStates.waiting_for_message_type)
async def handle_book_notification(message: types.Message):
    """Обработка уведомления о просрочке книги"""
    await message.answer(
        "📚 Уведомление о скорой просрочке сдачи книги\n\n"
        "Через сколько дней будет просрочена сдача книги?",
        reply_markup=get_days_keyboard()
    )
    await AdminStates.waiting_for_book_days.set()


@dp.message_handler(lambda message: message.text in ["1 день", "3 дня", "5 дней"],
                    state=AdminStates.waiting_for_book_days)
async def handle_book_days(message: types.Message, state: FSMContext):
    """Обработка выбора дней для книги"""
    days_text = message.text
    days_map = {"1 день": 1, "3 дня": 3, "5 дней": 5}
    days = days_map[days_text]

    await state.update_data(book_days=days)
    await message.answer(
        f"📝 Введите название книги:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await AdminStates.waiting_for_book_title.set()


@dp.message_handler(state=AdminStates.waiting_for_book_title)
async def handle_book_title(message: types.Message, state: FSMContext):
    """Обработка названия книги"""
    book_title = message.text.strip()
    if not book_title:
        await message.answer("❌ Пожалуйста, введите название книги:")
        return

    await state.update_data(book_title=book_title)
    await message.answer(
        "📋 Теперь введите номер читательского билета пользователя:"
    )
    await AdminStates.waiting_for_reader_ticket_for_book.set()


@dp.message_handler(state=AdminStates.waiting_for_reader_ticket_for_book)
async def handle_reader_ticket_for_book(message: types.Message, state: FSMContext):
    """Обработка номера читательского билета для книги"""
    reader_ticket = message.text.strip()

    # Ищем пользователя в базе
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id_tg FROM library_users WHERE id_reader_ticket = ?', (reader_ticket,))
        user = cursor.fetchone()

        if not user:
            await message.answer("❌ Пользователь с таким номером читательского билета не найден.")
            return

        user_id = user[0]
        data = await state.get_data()
        days = data['book_days']
        book_title = data['book_title']

        # Формируем сообщение для пользователя
        if days == 1:
            days_text = "завтра"
        else:
            days_text = f"через {days} {get_day_word(days)}"

        user_message = (
            f"📚 Уведомление от библиотеки\n\n"
            f"Книга <b>«{book_title}»</b> должна быть сдана {days_text}!\n\n"
            f"⚠️ Пожалуйста, не забудьте вернуть книгу в срок."
        )

        # Отправляем сообщение пользователю
        try:
            await bot.send_message(user_id, user_message, parse_mode="HTML")
            await message.answer(
                f"✅ Уведомление отправлено пользователю с читательским билетом {reader_ticket}",
                reply_markup=get_admin_keyboard()
            )
        except Exception as e:
            await message.answer(f"❌ Не удалось отправить сообщение пользователю: {e}")

        await AdminStates.waiting_for_message_type.set()

    finally:
        conn.close()


@dp.message_handler(lambda message: message.text == "🎫 Скоро завершится действие читательского билета",
                    state=AdminStates.waiting_for_message_type)
async def handle_ticket_notification(message: types.Message):
    """Обработка уведомления о завершении читательского билета"""
    await message.answer(
        "🎫 Уведомление о скором завершении читательского билета\n\n"
        "Через сколько дней завершится действие билета?",
        reply_markup=get_days_keyboard()
    )
    await AdminStates.waiting_for_ticket_days.set()


@dp.message_handler(lambda message: message.text in ["1 день", "3 дня", "5 дней"],
                    state=AdminStates.waiting_for_ticket_days)
async def handle_ticket_days(message: types.Message, state: FSMContext):
    """Обработка выбора дней для билета"""
    days_text = message.text
    days_map = {"1 день": 1, "3 дня": 3, "5 дней": 5}
    days = days_map[days_text]

    await state.update_data(ticket_days=days)
    await message.answer(
        "📋 Введите номер читательского билета пользователя:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await AdminStates.waiting_for_reader_ticket_for_ticket.set()


@dp.message_handler(state=AdminStates.waiting_for_reader_ticket_for_ticket)
async def handle_reader_ticket_for_ticket(message: types.Message, state: FSMContext):
    """Обработка номера читательского билета для уведомления о билете"""
    reader_ticket = message.text.strip()

    # Ищем пользователя в базе
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id_tg FROM library_users WHERE id_reader_ticket = ?', (reader_ticket,))
        user = cursor.fetchone()

        if not user:
            await message.answer("❌ Пользователь с таким номером читательского билета не найден.")
            return

        user_id = user[0]
        data = await state.get_data()
        days = data['ticket_days']

        # Формируем сообщение для пользователя
        if days == 1:
            days_text = "завтра"
        else:
            days_text = f"через {days} {get_day_word(days)}"

        user_message = (
            f"🎫 Уведомление от библиотеки\n\n"
            f"Срок действия вашего читательского билета истекает {days_text}!\n\n"
            f"⚠️ Пожалуйста, посетите библиотеку для продления билета."
        )

        # Отправляем сообщение пользователю
        try:
            await bot.send_message(user_id, user_message, parse_mode="HTML")
            await message.answer(
                f"✅ Уведомление отправлено пользователю с читательским билетом {reader_ticket}",
                reply_markup=get_admin_keyboard()
            )
        except Exception as e:
            await message.answer(f"❌ Не удалось отправить сообщение пользователю: {e}")

        await AdminStates.waiting_for_message_type.set()

    finally:
        conn.close()


@dp.message_handler(lambda message: message.text == "📢 Отправить иное уведомление",
                    state=AdminStates.waiting_for_message_type)
async def handle_custom_notification(message: types.Message):
    """Обработка кастомного уведомления"""
    await message.answer(
        "📢 Отправка произвольного уведомления\n\n"
        "Введите текст уведомления:",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await AdminStates.waiting_for_custom_message.set()


@dp.message_handler(state=AdminStates.waiting_for_custom_message)
async def handle_custom_message_text(message: types.Message, state: FSMContext):
    """Обработка текста кастомного уведомления"""
    custom_text = message.text.strip()
    if not custom_text:
        await message.answer("❌ Пожалуйста, введите текст уведомления:")
        return

    await state.update_data(custom_text=custom_text)
    await message.answer(
        "📋 Теперь введите номер читательского билета пользователя:"
    )
    await AdminStates.waiting_for_reader_ticket_for_custom.set()


@dp.message_handler(state=AdminStates.waiting_for_reader_ticket_for_custom)
async def handle_reader_ticket_for_custom(message: types.Message, state: FSMContext):
    """Обработка номера читательского билета для кастомного уведомления"""
    reader_ticket = message.text.strip()

    # Ищем пользователя в базе
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id_tg FROM library_users WHERE id_reader_ticket = ?', (reader_ticket,))
        user = cursor.fetchone()

        if not user:
            await message.answer("❌ Пользователь с таким номером читательского билета не найден.")
            return

        user_id = user[0]
        data = await state.get_data()
        custom_text = data['custom_text']

        # Формируем сообщение для пользователя
        user_message = (
            f"📢 Уведомление от библиотеки\n\n"
            f"{custom_text}"
        )

        # Отправляем сообщение пользователю
        try:
            await bot.send_message(user_id, user_message, parse_mode="HTML")
            await message.answer(
                f"✅ Уведомление отправлено пользователю с читательским билетом {reader_ticket}",
                reply_markup=get_admin_keyboard()
            )
        except Exception as e:
            await message.answer(f"❌ Не удалось отправить сообщение пользователю: {e}")

        await AdminStates.waiting_for_message_type.set()

    finally:
        conn.close()


# Вспомогательные функции
def get_day_word(days):
    """Получение правильной формы слова 'день'"""
    if days == 1:
        return "день"
    elif 2 <= days <= 4:
        return "дня"
    else:
        return "дней"


# Обработка любых других сообщений
@dp.message_handler()
async def handle_other_messages(message: types.Message):
    """Обработка любых других сообщений"""
    if is_admin(message.from_user.id):
        await message.answer(
            "Для работы с уведомлениями используйте команду /message",
            reply_markup=get_admin_keyboard()
        )
    else:
        await message.answer(
            "Для начала работы с ботом используйте команду /start\n\n"
            "📢 <i>Бот предназначен для уведомлений о сроке сдачи книг "
            "и продлении читательского билета</i>",
            parse_mode="HTML"
        )


# Запуск бота
async def on_startup(_):
    """Действия при запуске бота"""
    init_database()
    logger.info("Bot started successfully")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)