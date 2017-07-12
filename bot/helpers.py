#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Ricardo Ruiz

import json
import time


class EmptyFile(Exception):
    pass

class ActionHelpers(object):

    def __init__(self, bot):

        self.bot = bot

    def typing_wait(self, chatid, sleeptime=1):

        self.bot.send_chat_action(chatid, 'typing')
        time.sleep(sleeptime)

    def typing(self, send_text):

        def decorator(message):
            self.typing_wait(message.chat.id)
            send_text(message)

        return decorator

    def uploading(self, doctype):

        def decorator(send_document):

            def wrapper(message):

                action = 'upload_' + doctype
                self.bot.send_chat_action(message.chat.id, action)
                send_document(message)

            return wrapper

        return decorator


def load_data(datafile='data.json'):
    """Returns a dictionary with the json data"""

    with open(datafile, 'r') as data:

        content = data.read()
        if content:
            return json.loads(content)
        else:
            return {}

def add_data(data, datafile='data.json'):
    """Write data in the end of a json file"""

    with open(datafile, 'w') as datafile:
        datafile.write(json.dumps(data))