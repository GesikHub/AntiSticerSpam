import telebot
from flask import Flask, request
from datetime import datetime, timedelta
import time
import os

TOKEN = "413055169:AAEFwg2vGyprcAWzGE5x1gXhyHeZxCLHGhk"

bot = telebot.TeleBot(TOKEN)
admin = [273353288]
server = Flask(__name__)

users = {}

@bot.message_handler(content_types=['sticker'])
def sticker(message):
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

@server.route("/496468401:AAHFcONahk7qno39ovLwyH9O4EwEloEc138", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://antisticersbot.herokuapp.com/496468401:AAHFcONahk7qno39ovLwyH9O4EwEloEc138")
    return "!", 200

server.run(host="0.0.0.1", port=os.environ.get('PORT', 5002))
