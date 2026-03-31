import sqlite3
import telebot

bot = telebot.TeleBot('8389078868:AAFhYOHsn_34KMAouqJmnQprW3SXMlh9gCY')
#словарь для врем данных
user_data = {}

#созд баз
def init_database():

    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            userId INT,
            fname TEXT,
            lname TEXT,
            gender TEXT,
            username TEXT,
            UNIQUE(userId)
  );''')

    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute('''
            INSERT OR IGNORE INTO users (userId, fname, lname, gender)
            VALUES (1000, 'Alex', 'Smith', 'male')
        ''')
        print('добавлен новый пользователь')

    conn.commit()
    conn.close()
    print('база данных инициализирована успешно')


#просмотр что есть
def show_users():
    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        print("\n пользователи в БД:")
        if users:
            for user in users:
                print(f" ID: {user[0]}, Имя: {user[1]}, Фамилия: {user[2]}, Пол: {user[3]}")
        else:
            print("пользователей нет")

        conn.close()

    except sqlite3.Error as e:
        print(f"ошибка при получении пользователей: {e}")


#добав пользователя в бд
def add_user_to_db(user_id, first_name, last_name, username, gender=None):
    try:
        conn = sqlite3.connect('user_db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR IGNORE INTO users(userId, fname, lname, username, gender)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, first_name, last_name, username, gender))

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"ошибка при добавлении пользователя: {e}")
        return  False

#удаление из дб по ид
def delete_user_from_db(user_id):
    try:
        conn = sqlite3.connect('user_db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE userId = ?", (user_id))
        user = cursor.fetchone()

        if user:
            cursor.execute('DELETE FROM users WHERE userId = ?', (user_id))
            conn.commit()
            conn.close()
            return True, user
        else:
            conn.close()
            return False, None

    except sqlite3.Error as e:
        print(f"ошибка при удалении пользователя: {e}")
        return  False, None

#созд нов табл
def create_new_table(table_names, colums): pass

#получение инфы о табл
def get_table_info(table_name): pass

#в терминале далее необходимо создать базу данных
# sqlite3
# .save users.db
# .exit
def connect_db(db_name):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    return connect, cursor

async def stsrt_db(user):
    connect, cursor = connect_db('users_db')
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
  userId INT,
  fname TEXT,
  lname TEXT,
  gender TEXT,
  UNIQUE(userId)
  );''')
    connect.comit()
    cursor.execute('''INSERT INTO users(userId,fname,lname,gender)
	VALUES(100,'SSS','ser','w')''')

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ""
    username = message.from_user.username or ""

    add_user_to_db(user_id, first_name, last_name, username)

    welcome_text = f"привет, {first_name}! \n\n"
    welcome_text += f"/users - показать всех пользователей\n"
    welcome_text += f"/adduser - добавить нового пользователя\n"
    welcome_text += f"/deluser - удалить пользователя\n"
    welcome_text += f"/createtable - создать новую таблицу\n"
    welcome_text += f"/viewtable - посмотреть содержимое таблицы\n"
    welcome_text += f"/myid - показать мой ид\n"

    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['myid'])
def myid_command(message):
    bot.reply_to(message, f"ваш ид: "
                          f"{message.from_user.id}")

@bot.message_handler(commands=['users'])
def show_user_command(message):
    try:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()

        cursor.execute("SELECT userId, fname, lname, username, gender FROM users")
        users = cursor.fetchall()
        if users:
            respone = "список пользователей: \n"
            respone += '-' * "30" + "\n"
            for user in users:
                respone += f"**ID:** {user[0]}\n"
                respone += (f"**имя:** {user[1]}"
                            f"{user[2]}\n")
                respone += (f"**пол:**"
                            f"{user[3] if user[3] else 'не указан'}\n")
                respone += (f"**Username:** @"
                            f"{user[4] if user[4] else 'нет'}\n")
                respone += '-' * "30" + "\n"
        else:
            respone = "пользователей пока нет"

        conn.close()
        bot.reply_to(message, respone, parse_mode='Markdown')

    except sqlite3.Error as e:
            print(f"ошибка при добавлении пользователя: {e}")



@bot.message_handler(commands=['adduser'])
def add_user_start(message): pass

@bot.message_handler(commands=['deluser'])
def delete_user_start(message): pass

@bot.message_handler(commands=['stop'])
def start(message, fes=False):
    bot.send_message(message.chat.id, 'бе')

@bot.message_handler(content_types=['text'])
def get_text_message(message):

    bot.send_message(message.chat.id, 'привет')

if __name__ ==  '__main__':
    print("запуск бота...")

    init_database()
    show_users()

    print("\n бот запущен и готов к работе...")
    print(
        "доступ команды: /start, /users, /adduser, /deluser, /stop"
    )

bot.polling(none_stop=True, interval=0)