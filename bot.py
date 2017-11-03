import telebot
from datetime import datetime, timedelta
import time

TOKEN = "496468401:AAHFcONahk7qno39ovLwyH9O4EwEloEc138"

bot = telebot.TeleBot(TOKEN)
admin = [273353288]

users = {}

@bot.message_handler(content_types=['sticker'])
def sticker(message):
    if not (message.from_user.id in admin):
        if message.from_user.id in users:
            if datetime.now() - users[message.from_user.id][0] > timedelta(seconds=60):
                users[message.from_user.id][0] = datetime.now()
                users[message.from_user.id][1] = 1
            else:
                users[message.from_user.id][1] += 1
                if users[message.from_user.id][1] == 3:
                    bot.restrict_chat_member(message.chat.id, message.from_user.id, until_date=time.time() + 60)
                    del users[message.from_user.id]
        else:
            users[message.from_user.id] = [datetime.now(), 1]

bot.polling()
