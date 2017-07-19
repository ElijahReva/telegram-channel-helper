from time import sleep

import logging
import telegram
from configLoader import load, Settings

from telegram.error import NetworkError, Unauthorized
from telethon.tl.functions.channels.get_participants import \
    GetParticipantsRequest
from telethon.tl.types import Channel, User
from telethon.tl.types.channel_participants_recent import \
    ChannelParticipantsRecent
from telethon.tl.types.channels import ChannelParticipants
from telethon.tl.types.input_channel import InputChannel
from telethon.tl.types.messages.chats import Chats

from bot import Bot


update_id = None
logger = None


def main(settings: Settings):
    global update_id
    bot = telegram.Bot(settings["botKey"])

    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    while True:
        try:
            echo(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            update.message.reply_text(update.message.text)


def printChannel(channel: Channel):
    print(channel.id, channel.title)


def printParticipants(participants: ChannelParticipants):
    print("Count - ", participants.count)
    for user in participants.users:
        printUser(user)


def printUser(user: User):
    print(user.id, user.username)


def getUsers(chats: Chats):
    chat = chats.chats[0]
    printChannel(chat)

    inputChannel = InputChannel(chat.id, chat.access_hash)
    request = GetParticipantsRequest(
        inputChannel, ChannelParticipantsRecent(), 0, 5)
    # result = client(request)
    result = ''
    printParticipants(result)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    settings = load()

    bot = Bot(settings)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.

    bot.updater.idle()

    # allChannelRequest = GetAdminedPublicChannelsRequest()
    # res = client(allChannelRequest)
    # getUsers(res)
    # main(settings)
