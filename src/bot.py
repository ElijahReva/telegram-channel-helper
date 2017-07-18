import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

from src.apiclient import ApiClient
from src.bothelper import BotHelper
from src.configLoader import Settings


class Bot(object):

    CODE = range(1)

    def __init__(self, settings: Settings):
        self.api_key = settings['botKey']
        self.logger = logging.getLogger("bot")
        self.helper = BotHelper()
        self.api = ApiClient('ilya', settings['phone'], settings['api_id'], settings['api_hash'])

        self.updater = Updater(self.api_key)

        # Get the dispatcher to register handlers
        dp = self.updater.dispatcher

        # Add conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],

            states={
                self.CODE: [MessageHandler(Filters.forwarded, self.code)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        dp.add_handler(conv_handler)

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        self.updater.start_polling()

    def start(self, bot,  update):

        update.message.reply_text(
            'Hi! Forward code to me. '
            'Send /cancel to stop talking to me.\n\n')

        if self.api.sendcode():
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

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"' % (update, error))
