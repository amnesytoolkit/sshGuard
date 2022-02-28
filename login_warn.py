import requests
import datetime
import os
import random, time
import subprocess
from telegram_credentials import TELEGRAM_API_TOKEN, \
                                 TELEGRAM_USERS_TO_NOTIFY, \
                                 TELEGRAM_USERS_AUTHORIZED

from telegram.ext import Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
updater = Updater(token=TELEGRAM_API_TOKEN)
bot = updater.bot
dispatcher = updater.dispatcher


# ----- NOTIFY THE USER -----
# Get env variables
login_data = os.getenv("SSH_CONNECTION").split(" ")
username = os.getenv("USER")
source_ip = login_data[0]
server_ip = login_data[2]
port = login_data[3]
# supposing the script is runned at the time of the login,
# registering the current time as the login time should be enough.
date_of_login = str(datetime.datetime.now() )

# assemble the text
notify_text = "A new user has just logged on your server as " + username +\
    "\n\nsource_ip = " + source_ip + "\n" + \
    "server_ip = " + server_ip + "\n" + \
    "port = " + port + "\n" + \
    "date_of_login = " + port + "\n"

# send the message to every user on the specified list
for id_ in TELEGRAM_USERS_TO_NOTIFY:
    bot.send_message(chat_id=id_, text=notify_text)

# ----- 2FA AUTH THE USER -----
# clear the screen
os.system("clear")
try:
    authcode = str(random.randint(0, 99999999))
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Authenticate", callback_data="1"),
                                          InlineKeyboardButton("Cancel", callback_data="0")]])
    for id_ in TELEGRAM_USERS_AUTHORIZED:
        bot.send_message(chat_id=id_, text="Would you like to authorize the login on " + str(server_ip) + "?",
                         reply_markup=reply_markup)
    time.sleep(20)
    if os.getenv(authcode) == "1":
        os.system("clear")
        print("Login authorized!")
        os.system("clear")
    else:
        raise ValueError

except KeyboardInterrupt:
    subprocess.run("killall ssh", shell=True)
    subprocess.run("systemctl start sshd", shell=True)

def callback_query_handler(update, dispatcher):
    query = update.callback_query
    query.answer()
    if query.data == "1":
        bot.send_message(chat_id=query.message.chat_id, text="Authentication successful")
        os.environ[authcode] = "1"
    elif query.data == 0:
        bot.send_message(chat_id=query.message.chat_id, text="Canceled")
        subprocess.run("killall ssh", shell=True)
        subprocess.run("systemctl start sshd", shell=True)
    else:
        bot.send_message(chat_id=query.message.chat_id, text="Wrong auth choice")
        subprocess.run("killall ssh", shell=True)
        subprocess.run("systemctl start sshd", shell=True)


dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))

