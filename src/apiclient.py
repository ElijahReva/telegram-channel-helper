import logging

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError


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

    def sendcode(self):
        logging.info('OpenAPIConnection')
        if not self.client.connect():
            logging.info('OpenAPIConnection')
            if not self.client.connect():
                logging.info('Could not connect to Telegram servers.')
                return

        # Then, ensure we're authorized and have access
        authorized = self.is_user_authorized()
        logging.info('AlreadyAuthorized')
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
