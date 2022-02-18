import requests
import datetime
import os
import random
import subprocess
from telegram_credentials import TELEGRAM_API_TOKEN, \
                                 TELEGRAM_USERS_TO_NOTIFY, \
                                 TELEGRAM_USERS_AUTHORIZED

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
for id in TELEGRAM_USERS_TO_NOTIFY:
    requests.get("https://api.telegram.org/bot" + str(TELEGRAM_API_TOKEN)
                 + "/sendMessage?chat_id=" + str(id) + "&text=" + str(notify_text))

# ----- 2FA AUTH THE USER -----
# clear the screen
os.system("clear")
try:
    authcode = str(random.randint(0, 99999999))
    for id in TELEGRAM_USERS_AUTHORIZED:
        requests.get("https://api.telegram.org/bot" + str(TELEGRAM_API_TOKEN)
                     + "/sendMessage?chat_id=" + str(id) + "&text=" +
                     "Your 2FA code to login on " + str(server_ip) + " is " + str(authcode))
    login_code = input("Insert the code that we sent to your telegram account: ")
    if login_code != authcode:
        os.system("logout")

except KeyboardInterrupt:
    os.system("logout")