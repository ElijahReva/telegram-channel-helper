import json
import os
from os.path import expanduser
from pprint import pprint

homeFolder = expanduser("~")
settingsFolder = os.path.join(homeFolder, ".tlgchstat")
filePath = os.path.join(settingsFolder, "settings.json")


class Settings(object):
    def __init__(self):
        self.botKey = ""
        self.api_id = ""
        self.api_hash = ""
        self.channels = [12312312321, 123123123123]
        self.phone = '+380123456798'


def save(settings: Settings):
    with open(filePath, 'x', encoding='utf8') as outfile:
        raw_json = json.dumps(settings.__dict__,
                              indent=4,
                              sort_keys=True,
                              separators=(',', ': '),
                              ensure_ascii=False)
        outfile.write(raw_json)

def check_file():
    if not os.path.exists(settingsFolder):
        os.makedirs(settingsFolder)

    if not os.path.exists(filePath):
        default_settings = Settings()

        save(default_settings)

def load():
    check_file()
    with open(filePath) as data_file:
        data = json.load(data_file)
    pprint(data)
    return data
