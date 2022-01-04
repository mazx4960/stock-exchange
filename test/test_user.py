#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""
from user import *
from orders import *
import unittest


class TestUser(unittest.TestCase):
    def test_create_user(self):
        user = User("John")
        self.assertEqual(user.name, "John")
        self.assertEqual(len(user.orders), 0)

    def test_place_order(self):
        user = User("John")
        order = BuyOrder(user, "AAPL", 10, 10)
        user.place_order(order)
        self.assertEqual(len(user.orders), 1)
        self.assertEqual(user.orders[0], order)
