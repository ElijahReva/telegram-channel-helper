import logging

from typing import List
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels.get_admined_public_channels import  GetAdminedPublicChannelsRequest
from telethon.tl.types import Channel
from telethon.tl.types.messages import Chats


class ApiClient:
    def __init__(self,
                 session_user_id,
                 user_phone,
                 api_id, api_hash,
                 proxy=None):
        self.user_phone = user_phone
        self.client = TelegramClient(session_user_id, api_id, api_hash, proxy)

    def is_user_authorized(self):
        # Has the user been authorized yet
        # (code request sent and confirmed)?
        return self.client.session and self.client.get_me() is not None

    def reconnect(self):
        logging.info('Connecting to MTProto')
        if not self.client.connect():
            logging.info('OpenAPIConnection')
            if not self.client.connect():
                logging.info('Could not connect to Telegram servers.')
                return
        authorized = self.is_user_authorized()
        if authorized:
            logging.info("API Authorized")
        else:
            logging.info("API needs auth code")
        return authorized

    def send_code(self):

        authorized = self.reconnect()
        if not authorized:
            self.client.send_code_request(self.user_phone)
            return True
        else:
            return False

    def createSession(self, code):
        logging.info('CodeLogin')
        try:
            self.client.sign_in(self.user_phone, code)
            # Two-step verification may be enabled
        except SessionPasswordNeededError:
            return 0

    def get_dialogs(self) -> List[Channel]:
        request = GetAdminedPublicChannelsRequest()
        result = self.client(request)
        return result.chats

    def printDialogs(self, chats: Chats):
        for chat in chats:
            print(chat)
