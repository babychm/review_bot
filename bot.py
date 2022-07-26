#!/usr/bin/env python

import telebot
import config
import random
import requests
import mysql.connector

from mysql.connector import Error
from telebot import types
from config import db_config

def create_connection_mysql_db(db_host, user_name, user_password, db_name):
    connection_db = None
    try:
        connection_db = mysql.connector.connect(
            host = db_host,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("Подключение к MySQL успешно выполнено")
    except Error as db_connection_error:
        print("Возникла ошибка: ", db_connection_error)
    return connection_db

bot = telebot.TeleBot(config.token)

#class User:
#    def __init__(self, city):
#        self.city = city
#
#        keys = ['grade', 'feedback']
#
#        for key in keys:
#            self.key = None

@bot.message_handler(commands=['start'])
def step_contact_or_anon(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    item1 = types.KeyboardButton("Надіслати контакт", request_contact=True)
    item2 = types.KeyboardButton("Залишитись анонімним")

    markup.add(item1, item2)

    msg = bot.send_message(message.chat.id, "Надішліть мені Ваш номер телефону, щоб мені було зручніше з Вами спілкуватися", reply_markup=markup)

    conn = create_connection_mysql_db(db_config['mysql']['host'], db_config['mysql']['user'], db_config['mysql']['passwd'], db_config['mysql']['database'])

    cursor = conn.cursor()
    create_bots_user_query = "INSERT INTO users (telegram_id) VALUES('" + str(message.chat.id) + "');"
    cursor.execute(create_bots_user_query)
    conn.commit()
    bot.register_next_step_handler(msg, step_grade)

def step_grade(message):
    if message.text == 'Залишитись анонімним':
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'Добре, але мені буде не зручно з Вами спілкуватись')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        item4 = types.KeyboardButton("4")
        item5 = types.KeyboardButton("5")
        item6 = types.KeyboardButton("6")
        item7 = types.KeyboardButton("7")
        item8 = types.KeyboardButton("8")
        item9 = types.KeyboardButton("9")
        item10 = types.KeyboardButton("10")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
        msg = bot.send_message(message.chat.id, 'Оцініть, будь ласка, наскільки Вам сподобався останній візит до кліники?', reply_markup=markup)
        bot.register_next_step_handler(msg, step_after_grade)
    else:

        markup = types.ReplyKeyboardRemove(selective=False)
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        item1 = types.KeyboardButton("1")
        item2 = types.KeyboardButton("2")
        item3 = types.KeyboardButton("3")
        item4 = types.KeyboardButton("4")
        item5 = types.KeyboardButton("5")
        item6 = types.KeyboardButton("6")
        item7 = types.KeyboardButton("7")
        item8 = types.KeyboardButton("8")
        item9 = types.KeyboardButton("9")
        item10 = types.KeyboardButton("10")
        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
        msg = bot.send_message(message.chat.id, 'Оцініть, будь ласка, наскільки Вам сподобався останній візит до кліники?', reply_markup=markup)

        conn = create_connection_mysql_db(db_config['mysql']['host'], db_config['mysql']['user'], db_config['mysql']['passwd'], db_config['mysql']['database'])

        cursor = conn.cursor()
        set_user_phone_query = "UPDATE users SET phone_number='" + str(message.contact.phone_number) + "' WHERE telegram_id='"+ str(message.chat.id) + "';"
        cursor.execute(set_user_phone_query)
        conn.commit()
        bot.register_next_step_handler(msg, step_after_grade)

def step_after_grade(message):
    try:
        if message.text:
            if int(message.text) >= 8:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                url_button1 = types.InlineKeyboardButton(text="Клініка на Г.Кондрат'єва", url="https://g.page/uavets?share")
                url_button2 = types.InlineKeyboardButton(text="Клініка на Харківській", url="https://g.page/vetua?share")
                url_button3 = types.InlineKeyboardButton(text="Сторінка Facebook", url="https://facebook.com/vetua")
                url_button4 = types.InlineKeyboardButton(text="Профіль Facebook", url="https://facebook.com/uavets")
                url_button5 = types.InlineKeyboardButton(text="Профіль Instagram", url="https://instagram.com/uavet")
                keyboard.add(url_button1, url_button2, url_button3, url_button4, url_button5)
                bot.send_message(message.chat.id, 'Дякуємо Вам, нам також було приємно з Вами зустрітися. Оцініть також нас у Мережі:', reply_markup=keyboard)

                conn = create_connection_mysql_db(db_config['mysql']['host'], db_config['mysql']['user'], db_config['mysql']['passwd'], db_config['mysql']['database'])
                cursor = conn.cursor()
                set_review_query = "INSERT INTO reviews (phone_number,rate) VALUES('" + str(message.chat.id) + "', '"+ str(message.text) +"');"
                cursor.execute(set_review_query)
                conn.commit()

            elif int(message.text) <= 7:
                conn = create_connection_mysql_db(db_config['mysql']['host'], db_config['mysql']['user'], db_config['mysql']['passwd'], db_config['mysql']['database'])
                cursor = conn.cursor()
                set_review_query = "INSERT INTO reviews (phone_number,rate) VALUES('" + str(message.chat.id) + "', '" + str(message.text) + "');"
                cursor.execute(set_review_query)
                conn.commit()
                msg = bot.send_message(message.chat.id, 'Напишіть, будь ласка, що б Ви хотіли покращити в роботі клініки?')
                bot.register_next_step_handler(msg, step_review_text)
            # remove inline buttons
            #bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Дякую за відгук!", reply_markup=None)

    except Exception as e:
            print(repr(e))

def step_review_text(message):
    conn = create_connection_mysql_db(db_config['mysql']['host'], db_config['mysql']['user'], db_config['mysql']['passwd'], db_config['mysql']['database'])
    cursor = conn.cursor()
    set_review_query = "update reviews set text='" + str(message.text) + "' where id=(select id from reviews order by id desc limit 1);"
    cursor.execute(set_review_query)
    conn.commit()

# RUN
bot.polling(none_stop=True)
