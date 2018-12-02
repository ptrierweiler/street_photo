#!/usr/bin/python3
import logging
import os
import json
import datetime
from io import BytesIO
from picamera import PiCamera
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import telegram
import logging

# set logging
# set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

camera = PiCamera()

with open('token.json') as j:
    tj = json.load(j)    
    token = tj['token']
    path = tj['path'] 


def take_pict(path):
    camera.start_preview()
    now = datetime.datetime.now()
    output = str(now).split('.')[0].replace(' ','_').replace(':','') + '.jpg'
    out_path = os.path.join(path,output)
    camera.capture(out_path)
    camera.stop_preview()
    return out_path


def pict(bot, update):
    pic = take_pict(path)
    try:
        bot.send_photo(chat_id=update.message.chat_id, photo=open(pic, 'rb'))
    except telegram.error.TelegramError:
        retry_logic
    

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


updater = Updater(token=token)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start, Filters.user(username="@Ptrierweiler")))
dp.add_handler(CommandHandler("pict", pict, Filters.user(username="@Ptrierweiler")))




updater.start_polling()