#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""
import unittest

from orders import *
from user import *


class TestOrders(unittest.TestCase):
    def test_compare_buy_orders(self):
        order1 = BuyOrder(User("John"), "AAPL", 10, 10)
        order2 = BuyOrder(User("John"), "AAPL", 11, 10)
        self.assertLess(order2, order1)
    
    def test_compare_sell_orders(self):
        order1 = SellOrder(User("John"), "AAPL", 12, 10)
        order2 = SellOrder(User("John"), "AAPL", 13, 10)
        self.assertLess(order1, order2)

    def test_market_order(self):
        user = User("John")
        order = MarketOrder(user, "AAPL", 10, "BUY")
        self.assertEqual(order.user, user)
        self.assertEqual(order.ticker, "AAPL")
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.direction, "BUY")
        self.assertEqual(order.filled, 0)
        self.assertFalse(order.is_filled())
        self.assertEqual(str(order), "AAPL MKT BUY 0/10 PENDING")

    def test_limit_order(self):
        user = User("John")
        order = LimitOrder(user, "AAPL", 10, 10, "BUY")
        self.assertEqual(order.user, user)
        self.assertEqual(order.ticker, "AAPL")
        self.assertEqual(order.price, 10)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.direction, "BUY")
        self.assertEqual(order.filled, 0)
        self.assertFalse(order.is_filled())
        self.assertEqual(str(order), "AAPL LMT BUY $10.00 0/10 PENDING")

    def test_buy_order(self):
        user = User("John")
        order = BuyOrder(user, "AAPL", 10, 10)
        self.assertEqual(order.user, user)
        self.assertEqual(order.ticker, "AAPL")
        self.assertEqual(order.price, 10)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.direction, "BUY")
        self.assertEqual(order.filled, 0)
        self.assertFalse(order.is_filled())
        self.assertEqual(str(order), "AAPL LMT BUY $10.00 0/10 PENDING")

    def test_sell_order(self):
        user = User("John")
        order = SellOrder(user, "AAPL", 10, 10)
        self.assertEqual(order.user, user)
        self.assertEqual(order.ticker, "AAPL")
        self.assertEqual(order.price, 10)
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.direction, "SELL")
        self.assertEqual(order.filled, 0)
        self.assertFalse(order.is_filled())
        self.assertEqual(str(order), "AAPL LMT SELL $10.00 0/10 PENDING")
    
    def test_fill_market_order(self):
        user = User("John")
        order = MarketOrder(user, "AAPL", 10, "BUY")
        order.fill(10)
        self.assertEqual(order.filled, 10)
        self.assertTrue(order.is_filled())
        self.assertEqual(str(order), "AAPL MKT BUY 10/10 FILLED")
    
    def test_partial_fill_limit_order(self):
        user = User("John")
        order = LimitOrder(user, "AAPL", 10, 10, "BUY")
        order.fill(5)
        self.assertEqual(order.filled, 5)
        self.assertFalse(order.is_filled())
        self.assertEqual(str(order), "AAPL LMT BUY $10.00 5/10 PARTIAL")
