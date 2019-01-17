#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

import unittest
import config
from app import create_app

app = create_app()


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_list(self):
        self.app.get('/library/?keyword=国家地理')

    def test_get_detail(self):
        self.app.get('/library/book_detail?url=%2Fsearch%2Fdetail.action'
                     '%253Furl%253Dhttp%25253a%25252f%25252f61.142.33.201'
                     '%25253a8080%25252fopac_two%25252fsearch2%25252fs_de'
                     'tail.jsp%25253fsid%25253d0100015053%2526kw%253D%252'
                     '5e7%252599%2525be%2525e7%2525a7%252591%2525e5%25258'
                     '%2525a8%2525e4%2525b9%2525a6%2526searchtype%253D1%25'
                     '26page%253D1%2526xc%253D3')


if __name__ == '__main__':
    with app.app_context():
        unittest.main()
