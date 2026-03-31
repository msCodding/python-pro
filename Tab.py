import sqlite3
import telebot

bot_api = "8276664456:AAF6O4Xo2iWRKaDOsE7vNjvcrnov_PSdMFo"
bot = telebot.TeleBot(bot_api)


user_data = {}

def init_database():

    conn = sqlite3.connect('Cheliki.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Cheliki(
                            userId INT, 
                            fname TEXT,
                            lname TEXT,
                            age TEXT,
                            username TEXT,
                            profession TEXT,
                             UNIQUE(userId)
                             );''')

    cursor.execute("SELECT COUNT(*) FROM Cheliki")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
        INSERT OR IGNORE INTO Cheliki (userId, fname, lname, age, username, profession)
        VALUES (1, 'Alex', 'Smith', '29', 'asas', 'aaa') ''')
        print("Добавлен текстовый пользователь")

        conn.commit()
        conn.close()
        print("База данных инициализирована успешно")

def show_user():
    try:
        conn = sqlite3.connect('Cheliki.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Cheliki")
        users = cursor.fetchall()

        print("\n Пользователи в БД: ")
        if users:
            for user in users:
                print(f"    ID: {user[0]}, Имя: {user[1]}, "
                      f"Фамилия: {user[2]}, возраст: {user[3]}")
        else:
            print(" Пользователей нет")

        conn.close()

    except sqlite3.Error as e:
        print(f"Ошибка при получении пользователей: {e}")


def add_user_to_db(user_id, fname, lname, username, gender=None):
    try:
        conn = sqlite3.connect('users,db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO Cheliki (userId, fname, lname,
        username, gender)
        Values (?, ?, ?, ?, ?,)
        ''', (user_id, fname, lname, username, gender))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Ошибка")
        return  False

def delete_user_from_db(user_id):
    try:
        conn = sqlite3.connect('Cheliki.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Cheliki WHERE userId = ?", (user_id))
        user = cursor.fetchone()

        if user:
            cursor.execute("DELETE FROM Cheliki WHERE userId = ?", (user_id))
            conn.commit()
            conn.close()
            return True, user
        else:
            conn.close()
            return False, None
    except sqlite3.Error as e:
        print(f"Ошибка при удалении пользователя: {e}")

def create_new_table(table_name, columns): pass

def get_table_info(table_name): pass
def connect_db(db_name):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    return connect, cursor

async def start_db(user): pass

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or "🎉"
    username = message.from_user.username or "🎉"

    add_user_to_db(user_id, first_name, last_name, username)

    welcome_text = f"Привет, {first_name}! \n\n"
    welcome_text += "/users - показать всех пользователей"
    welcome_text += "/adduser - добавить нового пользователя\n"
    welcome_text += "deluser - удалить пользователя\n"
    welcome_text += "/createtable - создать новую таблицу\n"
    welcome_text += "/viewtable - посмотреть содержимое таблицы\n"
    welcome_text += "/myid - показать мой id\n"

    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['myid'])
def myid_command(message):
    bot.reply_to(message, f"Ваш ID: "
                          f"{message.from_user.id}")

@bot.message_handler(commands=['users'])
def show_users_command(message):
    try:
        conn = sqlite3.connect('Cheliki.db')
        cursor = conn.cursor()
        cursor.execute("SELECT userId, fname, lname, age, username, profession")
        users = cursor.fetchall()
        if users:
            response = "Список пользователей: \n"
            response += "-" * 30 + "\n"
            for user in users:
                response += (f" Id: {user[0]}\n")
                response += (f" Имя: {user[1]}" f" {user[2]}")
                response += (f" Пол:" f"{user[3] if user[3] else 'не указан'}\n")
                response += (f"Username: @" f"{user[4] if user[4] else 'нет'}")
                response += "-" * 30 + "\n"
        else:
            response = "Пользователей пока нет"

        conn.close()
        bot.reply_to(message, response, parse_mode="Markdown")
    except sqlite3.Error as e:
        bot.reply_to(message, f"Ошибка при получении данных: {e}")

@bot.message_handler(commands=['adduser'])
def add_users_start(message): pass

@bot.message_handler(commands=['deluser'])
def delete_users_start(message): pass

@bot.message_handler(content_types=['text'])
def handle_message(message): pass

if __name__ == "__main__":
    print("Запуск бота...")

    init_database()
    show_user()

    print("\n Бот готов к работе!")
    bot.polling(none_stop=True, interval=0)