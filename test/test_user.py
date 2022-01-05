#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""
from exchange import *
from user import *
from orders import *
import unittest


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.exchange = Exchange()

    def test_create_user(self):
        user = User("John", self.exchange)
        self.assertEqual(user.name, "John")
        self.assertEqual(len(user.orders), 0)

    def test_place_order(self):
        user = User("John", self.exchange)
        order = BuyOrder(user, "AAPL", 10, 10)
        user.place_order(order)
        self.assertEqual(len(user.orders), 1)
        self.assertEqual(user.orders[0], order)
    
    def test_deposit(self):
        user = User("John", self.exchange)
        user.deposit(100)
        self.assertEqual(user.get_balance(), 100)
    
    def test_withdraw(self):
        user = User("John", self.exchange)
        user.deposit(100)
        user.withdraw(50)
        self.assertEqual(user.get_balance(), 50)
    
    def test_withdraw_insufficient_balance(self):
        user = User("John", self.exchange)
        user.deposit(100)
        with self.assertRaises(Exception):
            user.withdraw(200)
    
    def test_add_stock(self):
        user = User("John", self.exchange)
        user.add_stock("AAPL", 1)
        self.assertEqual(user.portfolio["AAPL"], 1)
    
    def test_remove_stock(self):
        user = User("John", self.exchange)
        user.add_stock("AAPL", 1)
        user.remove_stock("AAPL", 1)
        self.assertEqual(user.portfolio["AAPL"], 0)
    
    def test_verify_order(self):
        user = User("John", self.exchange)
        user.add_stock("AAPL", 10)
        order = SellOrder(user, "AAPL", 10, 10)
        self.assertTrue(user.verify_order(order))
    
    def test_verify_order_diff_user(self):
        user1 = User("John", self.exchange)
        user2 = User("Jane", self.exchange)
        user1.add_stock("AAPL", 10)
        order = SellOrder(user2, "AAPL", 10, 10)
        self.assertFalse(user1.verify_order(order))
    
    def test_verify_order_insufficient_stock(self):
        user = User("John", self.exchange)
        user.add_stock("AAPL", 10)
        order = SellOrder(user, "AAPL", 10, 20)
        self.assertFalse(user.verify_order(order))
    
    def test_verify_order_insufficient_cash(self):
        user = User("John", self.exchange)
        user.deposit(100)
        order = BuyOrder(user, "AAPL", 10, 200)
        self.assertFalse(user.verify_order(order))


class TestAdmin(unittest.TestCase):
    def setUp(self) -> None:
        self.exchange = Exchange()

    def test_create_admin(self):
        user = Admin("John", self.exchange)
        self.assertEqual(user.name, "John")
        self.assertEqual(len(user.orders), 0)
    
    def test_deposit(self):
        user = Admin("John", self.exchange)
        user.deposit(100)
        self.assertEqual(user.get_balance(), 100)

    def test_withdraw(self):
        user = Admin("John", self.exchange)
        user.deposit(100)
        user.withdraw(50)
        self.assertEqual(user.get_balance(), 50)

    def test_withdraw_insufficient_balance(self):
        user = Admin("John", self.exchange)
        user.deposit(100)
        user.withdraw(200)
        self.assertEqual(user.get_balance(), 0)

    def test_add_stock(self):
        user = Admin("John", self.exchange)
        user.add_stock("AAPL", 1)
        self.assertEqual(user.portfolio["AAPL"], 1)

    def test_remove_stock(self):
        user = Admin("John", self.exchange)
        user.add_stock("AAPL", 1)
        user.remove_stock("AAPL", 2)
        self.assertEqual(user.portfolio["AAPL"], 0)

    def test_verify_order(self):
        user = Admin("John", self.exchange)
        order = SellOrder(user, "AAPL", 10, 10)
        self.assertTrue(user.verify_order(order))
