#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Ricardo Ruiz

from io import TextIOWrapper
from os import listdir
from os.path import isfile, join, basename
from random import choice
from helpers import load_data, add_data

class FileHandler(object):

    listfolder = staticmethod(lambda folder: [join(folder, file) for file in listdir(folder)
                                     if isfile(join(folder, file))])

    @staticmethod
    def _filepath(filename, search_folder):

        for path in search_folder:
            if filename == basename(path):
                return path

        raise IOError("File {} not found".format(filename))

    def __init__(self, media_folder='media',
        doctypes=['audios', 'photos', 'docs', 'extra'],
        json_data='../json/sent_files.json'):

        for doctype in doctypes:

            folder_name = join(media_folder, doctype)
            folder_files = self.listfolder(folder_name)

            setattr(self, doctype, folder_files)

        self.files = self.audios + self.photos + self.docs + self.extra

        self.actual_file = None
        self.sent_files = {}
        self.json_data = json_data

    def open(self, filename):
        """Return a file object or file_id if exists"""

        file_id = self.get_file_id(filename)

        if file_id:
            return file_id
        else:
            path = self._filepath(filename, self.files)
            self.actual_file = open(path, 'rb')
            return self.actual_file
 
    def random_path(self, type=None):

        if type:
            foldertype = getattr(self, type + 's')
            path = choice(foldertype)
        else:
            path = choice(self.files)

        return path

    def random_open(self, type=None):

        path = basename(self.random_path(type))

        return self.open(path)

    def get_file_id(self, filename):

        sent_files = load_data(datafile=self.json_data)
        return sent_files.get(filename)

    def add_file_id(self, filename, file_id):

        sent_files = load_data(datafile=self.json_data)
        sent_files[filename] = file_id

        add_data(sent_files, datafile=self.json_data)

    def close(self):

        if self.actual_file:
            self.actual_file.close()


class FileSender(object):

    def __init__(self, bot, filehandler=None, *args, **kwargs):

        self.bot = bot
        fh = filehandler
        self.file_handler = fh if fh else FileHandler(*args, **kwargs)
    
    def _get_photo_id(self, message):

        return message.photo[2].file_id

    def _get_audio_id(self, message):

        return message.audio.file_id

    def _get_document_id(self, message):

        return message.document.file_id

    def _get_file_id(self, message, type='photo'):

        get_type_id = getattr(self, "_get_{}_id".format(type))
        return get_type_id(message)

    def _add_file_id(self, message, filename, type):

        file_id = self._get_fileid(message, type)
        self.file_handler.add_file_id(filename, file_id)

    def _send_function(self, type):

        method = getattr(self.bot, "send_{type}".format(type=type))
        return method

    def send_file(self, chat_id, file_to_send, type):

        send_function = self._send_function(type)

        if isinstance(file_to_send, TextIOWrapper):    # Don't have file_id

            message = send_function(chat_id, file_to_send)
            file_id = self._get_file_id(message, type)
            self.file_handler.add_file_id(basename(file_to_send.name), file_id)

        else:                                 # We have file_id

            send_function(chat_id, file_to_send)

        self.file_handler.close()