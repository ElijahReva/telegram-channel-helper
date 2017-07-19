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
        print('Connecting to Telegram servers...')
        if not self.client.connect():
            print('Initial connection failed. Retrying...')
            if not self.client.connect():
                print('Could not connect to Telegram servers.')
                return

        # Then, ensure we're authorized and have access
        if not self.is_user_authorized():
            print('First run. Sending code request...')
            self.client.send_code_request(self.user_phone)
            return True
        else:
            print('Already singed')
            return False

            # self_user = None
            # while self_user is None:
            #     code = input('Enter the code you just received: ')
            #     try:
            #         self_user = self.client.sign_in(self.user_phone, code)
            #
            #     # Two-step verification may be enabled
            #     except SessionPasswordNeededError:
            #         pw = getpass('Two step verification is enabled. '
            #                      'Please enter your password: ')
            #
            #         self_user = self.client.sign_in(password=pw)

    def createSession(self, code):
        try:
            self.client.sign_in(self.user_phone, code)
            # Two-step verification may be enabled
        except SessionPasswordNeededError:
            return 0
