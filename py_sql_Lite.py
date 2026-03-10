import sqlite3
import telebot #pip install pytelegrambotapi
#в терминале далее необходимо создать саму базу данных
# sqlite3
# .save users.db
# .exit
def connect_db(db_name):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    return connect, cursor
async def start_db(user):
    connect, cursor = connect_db('users.db')
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users(
                    userId INT,
                    fname TEXT,
                    lname TEXT,
                    gender TEXT,
                    UNIQUE(userId)
                    );''')
    connect.commit()
    cursor.execute('''INSERT INTO users(userId,fname,lname,gender)
    VALUES(1000,'Alex','Smith','male');''')
# создать команды start/stop
bot_api = '8145235179:AAGWzxGYB2aQcsRneDR4Ks1ppQLt0hfzd4w'# ключ робота телеграм 🔑API - ключ для любых сайтов
Bot = telebot.TeleBot(bot_api)# подключение к самому роботу в тг

@Bot.message_handler(content_types=['text']) # определяем тип сообщений
def get_text_message(message):
    Bot.send_message(message.chat.id, 'Привет')

Bot.polling(none_stop=True,interval=0)# ВСЕГДА В КОНЦЕ
# бесконечное получение сообщение пока код запущен