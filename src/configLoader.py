import json
import os
from os.path import expanduser
from pprint import pprint


class Settings:
    def __init__(self):
        self.botKey = ""
        self.api_id = ""
        self.api_hash = ""
        self.channels = [12312312321, 123123123123]
        self.phone = '+380123456798'

    def __init__(self, bot_key, api_key, api_hash):
        self.botKey = bot_key
        self.api_id = api_key
        self.api_hash = api_hash
        self.channels = [12312312321, 123123123123]
        self.phone = '+380123456798'


class SettingsLoader:
    def __init__(self):
        self.homeFolder = expanduser("~")
        self.settingsFolder = os.path.join(self.homeFolder, ".tlgchstat")
        self.filePath = os.path.join(self.settingsFolder, "settings.json")

    def save(self, settings: Settings):
        with open(self.filePath, 'x', encoding='utf8') as outfile:
            raw_json = json.dumps(settings.__dict__,
                                  indent=4,
                                  sort_keys=True,
                                  separators=(',', ': '),
                                  ensure_ascii=False)
            outfile.write(raw_json)

    def check_file(self):
        if not os.path.exists(self.settingsFolder):
            os.makedirs(self.settingsFolder)

        if not os.path.exists(self.filePath):
            default_settings = Settings("BOT_KEY", "API_ID", "API_HASH")

            self.save(default_settings)

    def load(self):
        self.check_file()
        with open(self.filePath) as data_file:
            data = json.load(data_file)
        pprint(data)
        return data



