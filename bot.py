# run me from root folder: python run_longread_bot.py

import os
from datetime import datetime
import time
import logging
from telegram import Bot, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler, CallbackQueryHandler

import message_texts
from texts.longreads import Renderer

logger = logging.getLogger(__name__)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_LONGREAD")


class LongreadBot:

    lang = None
    bot = None
    text = None

    SET_LANG, GET = range(2)

    tasks_to_do = None

    def __init__(self, tasks_to_do):
        self.bot = Bot(token=TELEGRAM_TOKEN)
        self.tasks_to_do = tasks_to_do

    def start(self, update, context):
        keyboard = [[InlineKeyboardButton("Russian", callback_data='ru'),
                     InlineKeyboardButton("English", callback_data='en')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(text="Choose your language", reply_markup=reply_markup)

        return self.SET_LANG

    def set_lang(self, update, context):
        query = update.callback_query
        val = query.data
        choices = ['ru', 'en']
        if val not in choices:
            return ConversationHandler.END

        self.lang = val

        chat_id = query.message.chat_id
        self.bot.send_message(chat_id=chat_id, text=message_texts.MESSAGE_START(self.lang))

        return self.GET

    def get(self, update, context):
        text = update.message.text
        chat_id = update.message.chat["id"]

        task = {
            "text": text,
            "chat_id": chat_id,
            "timestamp": datetime.now().timestamp(),
        }
        self.tasks_to_do.put(task)
        return self.GET

    def render(self, tasks_to_do):

        while True:
            if tasks_to_do.empty():
                time.sleep(0.2)
                continue

            task = tasks_to_do.get()

            text = task["text"]
            chat_id = task["chat_id"]
            ts = task["timestamp"]

            time.sleep(0.2)

            if not tasks_to_do.empty():
                other_task = tasks_to_do.get()
                other_text = other_task["text"]
                other_chat_id = other_task["chat_id"]
                other_ts = other_task["timestamp"]

                if other_chat_id == chat_id and 0 < ts - other_ts < 0.5:
                    text = other_text + text
                elif other_chat_id == chat_id and -0.5 < ts - other_ts < 0:
                    text = text + other_text
                else:
                    tasks_to_do.put(other_task)

            r = Renderer()
            text, images = r.render(text)

            self.bot.send_message(chat_id=chat_id, text=text)

            if images:
                arr = []
                for it, image in enumerate(images):
                    arr.append(InputMediaPhoto(open(image, 'rb')))
                self.bot.send_media_group(chat_id=chat_id, media=arr)

                for image in images:
                    os.remove(image)

            self.bot.send_message(chat_id=chat_id, text=message_texts.RENDERED(self.lang))

    def done(self, update, context):
        return self.GET

    def main(self):
        updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
        dp = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.GET: [MessageHandler(Filters.regex('.*'), self.get, pass_user_data=True)],
                self.SET_LANG: [CallbackQueryHandler(self.set_lang, pass_user_data=True, pattern=r'.*')]
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), self.done)]
        )

        dp.add_handler(conv_handler)

        try:
            updater.start_polling()
            updater.idle()
        except Exception as e:
            print(f"Unexpected exception: {repr(e)}")
