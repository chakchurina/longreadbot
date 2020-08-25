# run me from root folder: python run_longread_bot.py

import os
import logging
from telegram import Bot, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, Filters, MessageHandler, CallbackQueryHandler

import message_texts
from texts.longreads import Renderer

logger = logging.getLogger(__name__)
# TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_LONGREAD")
TELEGRAM_TOKEN = '1058020278:AAHOjsOUikWdHdhTVtobV-Z2DKTiWWPE59A'


class LongreadBot:

    lang = None
    bot = None
    SET_LANG, RENDER = range(2)

    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)

    def start(self, update, context):
        keyboard = [[InlineKeyboardButton("Русский", callback_data='ru'),
                     InlineKeyboardButton("Английский", callback_data='en')]]
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

        return self.RENDER

    def render(self, update, context):
        text = update.message.text
        context.user_data['choice'] = text

        r = Renderer()
        text, images = r.render(text)
        update.message.reply_text(text)

        if images:
            chat_id = update.message.chat["id"]
            arr = []
            for it, image in enumerate(images):
                arr.append(InputMediaPhoto(open(image, 'rb')))
            self.bot.send_media_group(chat_id=chat_id, media=arr)

            for image in images:
                os.remove(image)

        update.message.reply_text(message_texts.RENDERED(self.lang))

        return self.RENDER

    def done(self, update, context):
        user_data = context.user_data
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_text("Bye!")

        user_data.clear()
        return ConversationHandler.END

    def main(self):
        updater = Updater(TELEGRAM_TOKEN, use_context=True)
        dp = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                self.RENDER: [MessageHandler(Filters.regex('.*'), self.render, pass_user_data=True)],
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
