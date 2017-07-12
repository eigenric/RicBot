#!/usr/bin/env python
# author: Ricardo Ruiz
# -*- coding: utf-8 -*-

import unittest
from bot.fileutils import FileHandler

class FileHandlerTest(unittest.TestCase):


    def __init__(self, *args, **kwargs):

        super(FileHandlerTest, self).__init__(*args, **kwargs)
        self.filehandler = FileHandler('../media')

    def test_open_close(self):
        """File handler can open and close ad file"""

        file = self.filehandler.open('pollito.jpg')
        self.filehandler.close()

        self.assertTrue(self.filehandler.actual_file.closed)
        self.assertTrue(file.closed)

    def test_add_fileid(self):

        self.filehandler.add_file_id('myfilename', 'filenameid')
        self.filehandler.add_file_id('otroarchivo', 'sucorrespondiente')
        self.filehandler.add_file_id('miultimo', 'caca')

    def test_get_fileid(self):

        self.assertEqual(
            self.filehandler.get_file_id('myfilename'), 'filenameid')
        self.assertEqual(
            self.filehandler.get_file_id('otroarchivo'), 'sucorrespondiente')
        self.assertEqual(
            self.filehandler.get_file_id('miultimo'), 'caca')


if __name__ == '__main__':

    unittest.main()