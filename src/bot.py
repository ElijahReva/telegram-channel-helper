import logging
from telegram.error import *

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
from telethon.tl.types import Channel

from typing import List

from apiclient import ApiClient
from bothelper import BotHelper
from configLoader import Settings


class Bot(object):

    CODE = range(1)

    def __init__(self, settings: Settings):
        self.api_key = settings['botKey']
        self.logger = logging.getLogger("bot")
        self.helper = BotHelper()
        self.api = ApiClient('ilya', settings['phone'], settings['api_id'], settings['api_hash'])

        self.api.reconnect()

        self.updater = Updater(self.api_key)

        # Get the dispatcher to register handlers
        self.dispatcher = self.updater.dispatcher

        # Add conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                self.CODE: [MessageHandler(Filters.forwarded, self.code)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        self.dispatcher.add_handler(CommandHandler('stats', self.stats))
        self.dispatcher.add_handler(conv_handler)

        # log all errors
        self.dispatcher.add_error_handler(self.error_callback)

        # Start the Bot
        self.updater.start_polling()
        self.logger.info("BotStarted")

    def stats(self, bot,  update):
        self.logger.info("Stats")
        dialogs = self.api.get_dialogs()
        message = Bot.channel_to_message(dialogs)
        update.message.reply_text(message)

    def start(self, bot,  update):
        self.logger.info("StartReceived")
        update.message.reply_text(
            'Hi!\n'
            'Send /cancel to stop talking to me.\n\n')

        if self.api.send_code():
            return self.CODE
        else:
            update.message.reply_text("You're already signed...\n"
                                      "Have a good day!")
            return ConversationHandler.END

    def code(self, bot, update):
        code = update.message.reply_text[17:22]
        self.api.createSession(code)

        return ConversationHandler.END

    def cancel(self, bot, update):
        user = update.message.from_user
        self.logger.info("User %s canceled the conversation." % user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def error_callback(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"' % (update, error))
        # try:
        #     raise error
        # except Unauthorized:
        # # remove update.message.chat_id from conversation list
        # except BadRequest:
        # # handle malformed requests - read more below!
        # except TimedOut:
        #
        # # handle slow connection problems
        # except NetworkError:
        #
        # #handle other connection problems
        # except ChatMigrated as e:
        #
        # # the chat_id of a group has changed, use e.new_chat_id instead
        # except TelegramError:


    @staticmethod
    def channel_to_message(channels: List[Channel]) -> str:
        lines = [str(i + 1) + ". " + ch.title for i, ch in enumerate(channels)]
        message = "Please select dialog\n" + "\n".join(lines)
        return message