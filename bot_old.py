#!/usr/bin/env python


import telebot
import config
import random
import requests

from telebot import types

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Надіслати контакт", request_contact=True)
    item2 = types.KeyboardButton("Залишитись анонімним")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, "Надішліть мені Ваш номер телефону, щоб мені було зручніше з Вами спілкуватися", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def lalala(message):
	if message.chat.type == 'private':
		if message.text == 'Залишитись анонімним':
			bot.send_message(message.chat.id, 'Добре, але мені буде не зручно з Вами спілкуватись')
			markup = types.InlineKeyboardMarkup(row_width=2)
			item1 = types.InlineKeyboardButton("1", callback_data='bad')
			item2 = types.InlineKeyboardButton("2", callback_data='bad')
			item3 = types.InlineKeyboardButton("3", callback_data='bad')
			item4 = types.InlineKeyboardButton("4", callback_data='bad')
			item5 = types.InlineKeyboardButton("5", callback_data='bad')
			item6 = types.InlineKeyboardButton("6", callback_data='bad')
			item7 = types.InlineKeyboardButton("7", callback_data='bad')
			item8 = types.InlineKeyboardButton("8", callback_data='good')
			item9 = types.InlineKeyboardButton("9", callback_data='good')
			item10 = types.InlineKeyboardButton("10", callback_data='good')

			markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)

			bot.send_message(message.chat.id, 'Оцініть, будь ласка, наскільки Вам сподобався останній візит до кліники?', reply_markup=markup)
		else:
            		bot.send_message(message.chat.id, 'Я Вас не розумію')

@bot.message_handler(content_types=['contact'])
def bebebe(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("1", callback_data='bad')
    item2 = types.InlineKeyboardButton("2", callback_data='bad')
    item3 = types.InlineKeyboardButton("3", callback_data='bad')
    item4 = types.InlineKeyboardButton("4", callback_data='bad')
    item5 = types.InlineKeyboardButton("5", callback_data='bad')
    item6 = types.InlineKeyboardButton("6", callback_data='bad')
    item7 = types.InlineKeyboardButton("7", callback_data='bad')
    item8 = types.InlineKeyboardButton("8", callback_data='good')
    item9 = types.InlineKeyboardButton("9", callback_data='good')
    item10 = types.InlineKeyboardButton("10", callback_data='good')

    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)

    bot.send_message(message.chat.id, 'Оцініть, будь ласка, наскільки Вам сподобався останній візит до кліники?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'good':
				keyboard = types.InlineKeyboardMarkup(row_width=1)
				url_button1 = types.InlineKeyboardButton(text="Клініка на Г.Кондрат'єва", url="https://g.page/uavets?share")
				url_button2 = types.InlineKeyboardButton(text="Клініка на Харківській", url="https://g.page/vetua?share")
				url_button3 = types.InlineKeyboardButton(text="Сторінка Facebook", url="https://facebook.com/vetua")
				url_button4 = types.InlineKeyboardButton(text="Профіль Facebook", url="https://facebook.com/uavets")
				url_button5 = types.InlineKeyboardButton(text="Профіль Instagram", url="https://instagram.com/uavet")
				keyboard.add(url_button1, url_button2, url_button3, url_button4, url_button5)
				bot.send_message(call.message.chat.id, 'Дякуємо Вам, нам також було приємно з Вами зустрітися. Оцініть також нас у Мережі:', reply_markup=keyboard)
			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'Напишіть, будь ласка, що б Ви хотіли покращити в роботі клініки?')

            # remove inline buttons
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Дякую за відгук!", reply_markup=None)

            # show alert
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

	except Exception as e:
		print(repr(e))

# RUN
bot.polling(none_stop=True)
