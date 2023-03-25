import requests
import datetime
import os
import random, time
import subprocess
from telegram_credentials import TELEGRAM_API_TOKEN, \
                                 TELEGRAM_USERS_TO_NOTIFY

telegram_url = "https://api.telegram.org/bot" + TELEGRAM_API_TOKEN \
               + "/sendMessage?chat_id="



# ----- NOTIFY THE USER -----
# Get env variables
login_data = os.getenv("SSH_CONNECTION").split(" ")
username = os.getenv("USER")
source_ip = login_data[0]
server_ip = login_data[2]
port = login_data[3]
# supposing the script is runned at the time of the login,
# registering the current time as the login time should be enough.
date_of_login = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# assemble the text
notify_text = "A new user has just logged on your server as " + username +\
    "\n\nsource_ip = " + source_ip + "\n" + \
    "server_ip = " + server_ip + "\n" + \
    "port = " + port + "\n" + \
    "date_of_login = " + date_of_login + "\n"

# send the message to every user on the specified list
for id_ in TELEGRAM_USERS_TO_NOTIFY:
     requests.get(telegram_url + str(id_) + "&text=" + str(notify_text))


