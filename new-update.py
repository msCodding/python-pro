import sqlite3
import telebot  # pip install pytelegrambotapi

# API ключ лучше хранить в переменных окружения, но для примера:
API_TOKEN = '8145235179:AAGWzxGYB2aQcsRneDR4Ks1ppQLt0hfzd4w'  # ВАЖНО: Смените ключ!
bot = telebot.TeleBot(API_TOKEN)

# Словарь для временного хранения данных
user_data = {}

#Инициализация базы данных и создание таблиц
def init_database():

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            userId INTEGER PRIMARY KEY,
            fname TEXT,
            lname TEXT,
            gender TEXT,
            username TEXT,
            UNIQUE(userId)
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
            INSERT OR IGNORE INTO users (userId, fname, lname, gender)
            VALUES (1000, 'Alex', 'Smith', 'male')
        ''')
        print("✅ Добавлен тестовый пользователь")

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована успешно")

#Функция для просмотра всех таблиц в БД
def show_all_tables():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("\n📊 Таблицы в базе данных:")
        for table in tables:
            print(f"  - {table[0]}")

            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()
            print("    Столбцы:")
            for col in columns:
                print(f"      {col[1]} ({col[2]})")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Ошибка при просмотре таблиц: {e}")

#Функция для просмотра всех пользователей
def show_users():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        print("\n👥 Пользователи в БД:")
        if users:
            for user in users:
                print(f"  ID: {user[0]}, Имя: {user[1]}, "
                      f"Фамилия: {user[2]}, Пол: {user[3]}")
        else:
            print("  Пользователей нет")

        conn.close()

    except sqlite3.Error as e:
        print(f"❌ Ошибка при получении пользователей: {e}")

#Добавление пользователя в БД
def add_user_to_db(user_id, first_name, last_name,
                   username, gender=None):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR IGNORE INTO users (userId, fname, lname,
             username, gender)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, first_name, last_name, username, gender))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"❌ Ошибка при добавлении пользователя: {e}")
        return False

#Удаление пользователя из БД по ID
def delete_user_from_db(user_id):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users "
                       "WHERE userId = ?", (user_id))
        user = cursor.fetchone()

        if user:
            cursor.execute("DELETE FROM users "
                           "WHERE userId = ?", (user_id,))
            conn.commit()
            conn.close()
            return True, user
        else:
            conn.close()
            return False, None

    except sqlite3.Error as e:
        print(f"❌ Ошибка при удалении пользователя: {e}")
        return False, None

#Получение следующего доступного ID для нового пользователя
def get_next_user_id():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(userId) FROM users")
        max_id = cursor.fetchone()[0]

        conn.close()

        if max_id:
            return max_id + 1
        else:
            return 1001

    except sqlite3.Error as e:
        print(f"❌ Ошибка при получении следующего ID: {e}")
        return 1001

#Создание новой таблицы
def create_new_table(table_name, columns):

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Формируем SQL запрос для создания таблицы
        columns_sql = []
        for col in columns:
            col_name = col['name']
            col_type = col['type']
            col_constraints = col.get('constraints', '')
            columns_sql.append(f"{col_name} {col_type} {col_constraints}")

        columns_str = ", ".join(columns_sql)
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

        cursor.execute(create_sql)
        conn.commit()
        conn.close()

        return True, create_sql
    except sqlite3.Error as e:
        return False, str(e)

#Получение информации о таблице
def get_table_info(table_name):

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]

        conn.close()

        return columns, row_count
    except sqlite3.Error as e:
        return None, 0

#Выполнение произвольного SQL запроса
def execute_custom_sql(sql_query):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute(sql_query)

        # Проверяем, был ли запрос SELECT
        if sql_query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            conn.close()
            return True, results
        else:
            conn.commit()
            conn.close()
            return True, None

    except sqlite3.Error as e:
        return False, str(e)


# Обработчики команд бота
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or "💥"
    username = message.from_user.username or ""

    add_user_to_db(user_id, first_name, last_name, username)

    welcome_text = f"Привет, {first_name}! 👋\n\n"
    welcome_text += "Я бот с базой данных. Доступные команды:\n"
    welcome_text += "/users - показать всех пользователей\n"
    welcome_text += "/adduser - добавить нового пользователя\n"
    welcome_text += "/deluser - удалить пользователя\n"
    welcome_text += "/tables - показать все таблицы\n"
    welcome_text += "/createtable - создать новую таблицу\n"
    welcome_text += "/viewtable - просмотреть содержимое таблицы\n"
    welcome_text += "/droptable - удалить таблицу\n"
    welcome_text += "/sql - выполнить SQL запрос\n"
    welcome_text += "/stats - статистика базы данных\n"
    welcome_text += "/myid - показать мой ID\n"
    welcome_text += "/help - помощь"

    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = "📚 Справка по командам:\n\n"
    help_text += "👤 **Управление пользователями:**\n"
    help_text += "/users - показать список всех пользователей\n"
    help_text += "/adduser - добавить нового пользователя\n"
    help_text += "/deluser - удалить пользователя по ID\n\n"

    help_text += "📊 **Управление таблицами:**\n"
    help_text += "/tables - показать все таблицы в БД\n"
    help_text += "/createtable - создать новую таблицу\n"
    help_text += "/viewtable - просмотреть содержимое таблицы\n"
    help_text += "/droptable - удалить таблицу\n"
    help_text += "/sql - выполнить произвольный SQL запрос\n\n"

    help_text += "ℹ️ **Другое:**\n"
    help_text += "/stats - показать статистику БД\n"
    help_text += "/myid - показать ваш Telegram ID\n"
    help_text += "/start - приветственное сообщение\n"
    help_text += "/help - эта справка"

    bot.reply_to(message, help_text, parse_mode='Markdown')


@bot.message_handler(commands=['myid'])
def myid_command(message):
    bot.reply_to(message, f"🆔 Ваш Telegram ID: "
                          f"{message.from_user.id}")


@bot.message_handler(commands=['users'])
def show_users_command(message):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT userId, fname, lname, "
                       "gender, username FROM users")
        users = cursor.fetchall()
        if users:
            response = "📋 **Список пользователей:**\n"
            response += "━" * 30 + "\n"
            for user in users:
                response += f"🆔 **ID:** {user[0]}\n"
                response += (f"👤 **Имя:** {user[1]}"
                             f" {user[2]}\n")
                response += (f"⚥ **Пол:** "
                             f"{user[3] if user[3] else 'не указан'}\n")
                response += (f"📱 **Username:** @"
                             f"{user[4] if user[4] else 'нет'}\n")
                response += "━" * 30 + "\n"
        else:
            response = "📭 Пользователей пока нет"

        conn.close()
        bot.reply_to(message, response, parse_mode=
        'Markdown')

    except sqlite3.Error as e:
        bot.reply_to(message, f"❌ Ошибка при получении "
                              f"данных: {e}")


#Показать все таблицы в базе данных
@bot.message_handler(commands=['tables'])
def show_tables_command(message):

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()

        if tables:
            response = "📊 **Таблицы в базе данных:**\n\n"
            for table in tables:
                table_name = table[0]
                columns, row_count = get_table_info(table_name)

                response += f"📁 **{table_name}**\n"
                response += f"   📝 Записей: {row_count}\n"
                response += f"   📌 Столбцы: {', '.join([col[1] for col in columns])}\n\n"
        else:
            response = "📭 В базе данных нет таблиц"

        conn.close()
        bot.reply_to(message, response, parse_mode='Markdown')

    except sqlite3.Error as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")


@bot.message_handler(commands=['stats'])
def stats_command(message):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        tables_count = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(page_count) FROM pragma_page_count()")
        db_size = cursor.fetchone()[0] or 0

        response = f"📊 **Статистика базы данных:**\n\n"
        response += f"👥 **Пользователей:** {users_count}\n"
        response += f"📁 **Таблиц:** {tables_count}\n"
        response += f"💾 **Размер БД:** ~{db_size * 4} KB\n"

        conn.close()
        bot.reply_to(message, response, parse_mode='Markdown')

    except sqlite3.Error as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

#Добавить пользователя
@bot.message_handler(commands=['adduser'])
def add_user_start(message):
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(message.chat.id,
                     "Введите имя нового пользователя:",
                     reply_markup=markup)
    user_data[message.chat.id] = {'state': 'waiting_fname'}

#Удалить пользователя
@bot.message_handler(commands=['deluser'])
def delete_user_start(message):
    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(message.chat.id,
                     "Введите ID пользователя "
                     "для удаления:",
                     reply_markup=markup)
    user_data[message.chat.id] = {'state':
                                      'waiting_delete_id'}

#Начало создания новой таблицы
@bot.message_handler(commands=['createtable'])
def create_table_start(message):

    markup = telebot.types.ForceReply(selective=False)

    instruction = "📝 **Создание новой таблицы**\n\n"
    instruction += "Введите название таблицы:\n"
    instruction += "(только латинские буквы и цифры)"

    bot.send_message(message.chat.id, instruction,
                     reply_markup=markup, parse_mode='Markdown')
    user_data[message.chat.id] = {'state': 'waiting_table_name'}

#Начало просмотра таблицы
@bot.message_handler(commands=['viewtable'])
def view_table_start(message):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()

        if tables:
            tables_list = "\n".join([f"• {t[0]}" for t in tables])
            instruction = f"📋 **Доступные таблицы:**\n\n{tables_list}\n\n"
            instruction += "Введите название таблицы для просмотра:"

            markup = telebot.types.ForceReply(selective=False)
            bot.send_message(message.chat.id, instruction,
                             reply_markup=markup, parse_mode='Markdown')
            user_data[message.chat.id] = {'state': 'waiting_view_table'}
        else:
            bot.reply_to(message, "📭 В базе данных нет таблиц")

    except sqlite3.Error as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

#Начало удаления таблицы
@bot.message_handler(commands=['droptable'])
def drop_table_start(message):
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'users'")
        tables = cursor.fetchall()
        conn.close()

        if tables:
            tables_list = "\n".join([f"• {t[0]}" for t in tables])
            instruction = f"⚠️ **Удаление таблицы**\n\n"
            instruction += f"Доступные таблицы для удаления (кроме users):\n{tables_list}\n\n"
            instruction += "Введите название таблицы для удаления:"

            markup = telebot.types.ForceReply(selective=False)
            bot.send_message(message.chat.id, instruction,
                             reply_markup=markup, parse_mode='Markdown')
            user_data[message.chat.id] = {'state': 'waiting_drop_table'}
        else:
            bot.reply_to(message, "📭 Нет таблиц для удаления (кроме users)")

    except sqlite3.Error as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

#Выполнение произвольного SQL запроса
@bot.message_handler(commands=['sql'])
def execute_sql_start(message):
    instruction = "🔧 **Выполнение SQL запроса**\n\n"
    instruction += "Введите SQL запрос:\n"
    instruction += "Пример: SELECT * FROM users;\n"
    instruction += "⚠️ Будьте осторожны с DELETE и DROP!"

    markup = telebot.types.ForceReply(selective=False)
    bot.send_message(message.chat.id, instruction,
                     reply_markup=markup, parse_mode='Markdown')
    user_data[message.chat.id] = {'state': 'waiting_sql'}

#Обработка всех текстовых сообщений
@bot.message_handler(content_types=["text"])
def handle_messages(message):

    chat_id = message.chat.id

    # Добавление пользователя
    if (chat_id in user_data and
            user_data[chat_id].
                    get('state') == 'waiting_fname'):
        user_data[chat_id]['fname'] = message.text
        user_data[chat_id]['state'] = 'waiting_lname'
        bot.send_message(chat_id, "Введите фамилию:",
                         reply_markup=telebot.types.
                         ForceReply(selective=False))

    elif (chat_id in user_data and user_data[chat_id].
            get('state') == 'waiting_lname'):
        user_data[chat_id]['lname'] = message.text
        user_data[chat_id]['state'] = 'waiting_gender'

        markup = (telebot.types.ReplyKeyboardMarkup
                  (resize_keyboard=True,
                   ne_time_keyboard=True))
        markup.add('male', 'female', 'other')
        bot.send_message(chat_id, "Выберите пол:",
                         reply_markup=markup)

    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_gender':
        gender = message.text.lower()
        if gender in ['male', 'female', 'other']:
            user_data[chat_id]['gender'] = gender
            user_data[chat_id]['state'] = 'waiting_username'
            bot.send_message(chat_id, "Введите username (или отправьте 'skip' чтобы пропустить):",
                             reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            bot.send_message(chat_id, "Пожалуйста, выберите пол из вариантов: male, female, other")

    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_username':
        username = message.text if message.text.lower() != 'skip' else ""

        new_id = get_next_user_id()

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO users (userId, fname, lname, gender, username)
                VALUES (?, ?, ?, ?, ?)
            ''', (new_id, user_data[chat_id]['fname'], user_data[chat_id]['lname'],
                  user_data[chat_id]['gender'], username))

            conn.commit()
            conn.close()

            bot.send_message(chat_id, f"✅ Пользователь успешно добавлен!\n"
                                      f"ID: {new_id}\n"
                                      f"Имя: {user_data[chat_id]['fname']} {user_data[chat_id]['lname']}")

        except sqlite3.Error as e:
            bot.send_message(chat_id, f"❌ Ошибка при добавлении пользователя: {e}")

        del user_data[chat_id]

    # Удаление пользователя
    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_delete_id':
        try:
            user_id = int(message.text)
            success, deleted_user = delete_user_from_db(user_id)

            if success:
                bot.send_message(chat_id, f"✅ Пользователь успешно удален!\n"
                                          f"Удален: {deleted_user[1]} {deleted_user[2]} (ID: {deleted_user[0]})")
            else:
                bot.send_message(chat_id, f"❌ Пользователь с ID {user_id} не найден")

        except ValueError:
            bot.send_message(chat_id, "❌ Пожалуйста, введите корректный числовой ID")
        except Exception as e:
            bot.send_message(chat_id, f"❌ Ошибка: {e}")

        del user_data[chat_id]

    # Создание новой таблицы
    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_table_name':
        table_name = message.text.strip()

        # Проверяем название таблицы
        if not table_name.isidentifier():
            bot.send_message(chat_id, "❌ Некорректное название таблицы. Используйте только латинские буквы и цифры")
            return

        user_data[chat_id]['table_name'] = table_name
        user_data[chat_id]['columns'] = []
        user_data[chat_id]['state'] = 'waiting_column_name'

        instruction = f"Создание таблицы **{table_name}**\n\n"
        instruction += "Введите название первого столбца (или 'готово' для завершения):"

        bot.send_message(chat_id, instruction, parse_mode='Markdown',
                         reply_markup=telebot.types.ForceReply(selective=False))

    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_column_name':
        if message.text.lower() == 'готово':
            if len(user_data[chat_id]['columns']) > 0:
                # Создаем таблицу
                success, result = create_new_table(
                    user_data[chat_id]['table_name'],
                    user_data[chat_id]['columns']
                )

                if success:
                    response = f"✅ Таблица **{user_data[chat_id]['table_name']}** успешно создана!\n\n"
                    response += "**Структура:**\n"
                    for col in user_data[chat_id]['columns']:
                        response += f"• {col['name']} {col['type']}\n"
                else:
                    response = f"❌ Ошибка при создании таблицы: {result}"

                bot.send_message(chat_id, response, parse_mode='Markdown')
                del user_data[chat_id]
            else:
                bot.send_message(chat_id, "❌ Таблица должна содержать хотя бы один столбец")
        else:
            user_data[chat_id]['current_column'] = {'name': message.text}
            user_data[chat_id]['state'] = 'waiting_column_type'

            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('INTEGER', 'TEXT', 'REAL', 'BLOB')
            bot.send_message(chat_id, "Выберите тип данных:", reply_markup=markup)

    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_column_type':
        col_type = message.text.upper()
        if col_type in ['INTEGER', 'TEXT', 'REAL', 'BLOB']:
            user_data[chat_id]['current_column']['type'] = col_type
            user_data[chat_id]['state'] = 'waiting_column_constraints'

            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add('PRIMARY KEY', 'NOT NULL', 'UNIQUE', 'без ограничений')
            bot.send_message(chat_id, "Выберите ограничения (или 'без ограничений'):", reply_markup=markup)
        else:
            bot.send_message(chat_id, "❌ Выберите тип из предложенных вариантов")

    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_column_constraints':
        constraints = message.text
        if constraints == 'без ограничений':
            user_data[chat_id]['current_column']['constraints'] = ''
        else:
            user_data[chat_id]['current_column']['constraints'] = constraints

        # Добавляем столбец
        user_data[chat_id]['columns'].append(user_data[chat_id]['current_column'])
        user_data[chat_id]['state'] = 'waiting_column_name'

        bot.send_message(chat_id,
                         f"✅ Столбец добавлен. Введите название следующего столбца (или 'готово'):",
                         reply_markup=telebot.types.ReplyKeyboardRemove())

    # Просмотр таблицы
    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_view_table':
        table_name = message.text.strip()

        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # Получаем данные
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 20")
            rows = cursor.fetchall()

            if rows:
                # Получаем названия столбцов
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in cursor.fetchall()]

                response = f"📋 **Содержимое таблицы {table_name}:**\n\n"
                response += " | ".join(columns) + "\n"
                response += "─" * 50 + "\n"

                for row in rows:
                    response += " | ".join([str(r) for r in row]) + "\n"

                if len(rows) == 20:
                    response += "\n*Показаны первые 20 записей*"
            else:
                response = f"📭 Таблица {table_name} пуста"

            conn.close()
            bot.send_message(chat_id, response, parse_mode='Markdown')

        except sqlite3.Error as e:
            bot.send_message(chat_id, f"❌ Ошибка: {e}")

        del user_data[chat_id]

    # Удаление таблицы
    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_drop_table':
        table_name = message.text.strip()

        if table_name == 'users':
            bot.send_message(chat_id, "❌ Нельзя удалить таблицу users")
        else:
            try:
                conn = sqlite3.connect('users.db')
                cursor = conn.cursor()

                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                conn.commit()
                conn.close()

                bot.send_message(chat_id, f"✅ Таблица {table_name} успешно удалена")

            except sqlite3.Error as e:
                bot.send_message(chat_id, f"❌ Ошибка: {e}")

        del user_data[chat_id]

    # Выполнение SQL запроса
    elif chat_id in user_data and user_data[chat_id].get('state') == 'waiting_sql':
        sql_query = message.text.strip()

        success, result = execute_custom_sql(sql_query)

        if success:
            if result is not None:  # Это был SELECT
                if result:
                    response = "✅ **Результат запроса:**\n\n"
                    for row in result[:10]:  # Показываем первые 10 строк
                        response += str(row) + "\n"

                    if len(result) > 10:
                        response += f"\n*Показаны первые 10 из {len(result)} записей*"
                else:
                    response = "📭 Запрос выполнен, но не вернул данных"
            else:
                response = "✅ Запрос успешно выполнен"
        else:
            response = f"❌ Ошибка: {result}"

        bot.send_message(chat_id, response, parse_mode='Markdown')
        del user_data[chat_id]

    else:
        bot.send_message(message.chat.id,
                         'Я понимаю только команды. Напишите /help для списка команд.')


# Инициализация БД при запуске
if __name__ == "__main__":
    print("🚀 Запуск бота...")

    init_database()
    #show_all_tables()
    show_users()

    print("\n🤖 Бот запущен и готов к работе...")
    print(
        "📝 Доступные команды: /start, /users, /adduser, "
        "/deluser, /tables, /createtable, /viewtable, "
        "/droptable, /sql, /stats, /myid, /help")
    bot.polling(none_stop=True, interval=0)