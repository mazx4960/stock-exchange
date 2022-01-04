#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""
from io import StringIO
import unittest
from unittest.mock import patch

from exchange import *
from orders import *
from user import *


BUY = 0
SELL = 1


class TestExchange(unittest.TestCase):
    def test_create_exchange(self):
        exchange = Exchange()
        self.assertEqual(len(exchange.stocks), 0)
        self.assertEqual(len(exchange.limit_orders), 0)
        self.assertEqual(len(exchange.market_orders), 0)
        self.assertEqual(len(exchange.trades), 0)

    def test_place_limit_order(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user = User("John")
        order = BuyOrder(user, "AAPL", 10, 10)
        exchange.place_limit_order(order)
        self.assertEqual(len(exchange.limit_orders), 1)
        self.assertEqual(exchange.limit_orders["AAPL"][BUY][0], order)

    def test_match_limit_orders(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        order1 = BuyOrder(user1, "AAPL", 10, 10)
        order2 = SellOrder(user2, "AAPL", 10, 10)
        exchange.place_limit_order(order1)
        exchange.place_limit_order(order2)
        self.assertEqual(len(exchange.limit_orders["AAPL"][BUY]), 0)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 0)

    def test_match_limit_orders_with_partial_fill(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        order1 = BuyOrder(user1, "AAPL", 10, 10)
        order2 = SellOrder(user2, "AAPL", 10, 5)
        exchange.place_limit_order(order1)
        exchange.place_limit_order(order2)
        self.assertEqual(len(exchange.limit_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 0)

    def test_match_market_orders(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        order1 = MarketOrder(user1, "AAPL", 10, "BUY")
        order2 = MarketOrder(user2, "AAPL", 10, "SELL")
        exchange.place_market_order(order1)
        exchange.place_market_order(order2)
        self.assertEqual(len(exchange.market_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.market_orders["AAPL"][SELL]), 1)

    def test_match_limit_and_market_orders(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        order1 = BuyOrder(user1, "AAPL", 10, 10)
        order2 = MarketOrder(user2, "AAPL", 10, "SELL")
        exchange.place_limit_order(order1)
        exchange.place_market_order(order2)
        self.assertEqual(len(exchange.market_orders["AAPL"][BUY]), 0)
        self.assertEqual(len(exchange.market_orders["AAPL"][SELL]), 0)

    def test_match_market_and_limit_orders(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        order1 = MarketOrder(user2, "AAPL", 10, "BUY")
        order2 = SellOrder(user1, "AAPL", 10, 10)
        exchange.place_market_order(order1)
        exchange.place_limit_order(order2)
        self.assertEqual(len(exchange.market_orders["AAPL"][BUY]), 0)
        self.assertEqual(len(exchange.market_orders["AAPL"][SELL]), 0)

    def test_match_multiple_orders(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        user3 = User("Jack")
        order1 = BuyOrder(user1, "AAPL", 10, 10)
        order2 = BuyOrder(user2, "AAPL", 11, 5)
        order3 = MarketOrder(user3, "AAPL", 6, "SELL")
        exchange.place_limit_order(order1)
        exchange.place_limit_order(order2)
        exchange.place_market_order(order3)
        self.assertEqual(len(exchange.limit_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 0)
        remaining_buy_order = exchange.limit_orders["AAPL"][BUY][0]
        self.assertEqual(remaining_buy_order.user, user1)
        self.assertEqual(remaining_buy_order.filled, 1)
        self.assertEqual(remaining_buy_order.price, 10)
    
    def test_match_multiple_orders_2(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        user3 = User("Jack")
        order1 = SellOrder(user1, "AAPL", 10, 5)
        order2 = SellOrder(user2, "AAPL", 11, 10)
        order3 = MarketOrder(user3, "AAPL", 6, "BUY")
        exchange.place_limit_order(order1)
        exchange.place_limit_order(order2)
        exchange.place_market_order(order3)
        self.assertEqual(len(exchange.limit_orders["AAPL"][BUY]), 0)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 1)
        remaining_sell_order = exchange.limit_orders["AAPL"][SELL][0]
        self.assertEqual(remaining_sell_order.user, user2)
        self.assertEqual(remaining_sell_order.filled, 1)
        self.assertEqual(remaining_sell_order.price, 11)

    def test_match_multiple_orders_2(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        user3 = User("Jack")
        order1 = MarketOrder(user1, "AAPL", 5, "BUY")
        order2 = MarketOrder(user2, "AAPL", 10, "BUY")
        order3 = SellOrder(user3, "AAPL", 50, 6)
        exchange.place_market_order(order1)
        exchange.place_market_order(order2)
        exchange.place_limit_order(order3)
        self.assertEqual(len(exchange.market_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 0)
        remaining_buy_order = exchange.market_orders["AAPL"][BUY][0]
        self.assertEqual(remaining_buy_order.user, user2)
        self.assertEqual(remaining_buy_order.filled, 1)

    def test_match_multiple_limit_orders(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user1 = User("John")
        user2 = User("Jane")
        user3 = User("Jack")
        order1 = BuyOrder(user1, "AAPL", 10, 10)
        order2 = BuyOrder(user2, "AAPL", 11, 5)
        order3 = SellOrder(user3, "AAPL", 10.5, 6)
        exchange.place_limit_order(order1)
        exchange.place_limit_order(order2)
        exchange.place_market_order(order3)
        # Only the second order should be filled
        self.assertEqual(len(exchange.limit_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 1)
        remaining_buy_order = exchange.limit_orders["AAPL"][BUY][0]
        self.assertEqual(remaining_buy_order, order1)
        remaining_sell_order = exchange.limit_orders["AAPL"][SELL][0]
        self.assertEqual(remaining_sell_order.user, user3)
        self.assertEqual(remaining_sell_order.filled, 5)
        # Order 3 should be filled at 11
        self.assertEqual(len(exchange.trades["AAPL"]), 1)
        self.assertEqual(exchange.trades["AAPL"][0].price, 11)

    def test_execute_limit_order(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user = User("John")
        exchange.execute(user, "BUY AAPL LMT $10 10")
        exchange.execute(user, "SELL AAPL LMT $11 10")
        self.assertEqual(len(exchange.limit_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 1)
        self.assertEqual(len(user.orders), 2)

    def test_execute_market_order(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user = User("John")
        exchange.execute(user, "BUY AAPL MKT 10")
        exchange.execute(user, "SELL AAPL MKT 10")
        self.assertEqual(len(exchange.market_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.market_orders["AAPL"][SELL]), 1)
        self.assertEqual(len(user.orders), 2)

    def test_execute_quote(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user = User("John")
        exchange.execute(user, "BUY AAPL LMT $10 10")
        exchange.execute(user, "SELL AAPL MKT 5")
        exchange.execute(user, "SELL AAPL LMT $11 10")
        self.assertEqual(len(exchange.limit_orders["AAPL"][BUY]), 1)
        self.assertEqual(len(exchange.limit_orders["AAPL"][SELL]), 1)
        self.assertEqual(len(user.orders), 3)
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exchange.execute(user, "QUOTE AAPL")
            self.assertEqual(fake_out.getvalue(),
                             "AAPL BID: $10.00 ASK: $11.00 LAST: $10.00\n")

    def test_execute_empty_quote(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user = User("John")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exchange.execute(user, "QUOTE AAPL")
            self.assertEqual(fake_out.getvalue(),
                             "AAPL BID: $0.00 ASK: $0.00 LAST: $0.00\n")

    def test_execute_view_orders(self):
        exchange = Exchange()
        aapl = Stock("AAPL")
        exchange.list_stock(aapl)
        user = User("John")
        exchange.execute(user, "BUY AAPL LMT $10 10")
        exchange.execute(user, "SELL AAPL LMT $11 10")
        with patch('sys.stdout', new=StringIO()) as fake_out:
            exchange.execute(user, "VIEW ORDERS")
            self.assertEqual(fake_out.getvalue(),
                             "1. AAPL LMT BUY $10.00 0/10 PENDING\n2. AAPL LMT SELL $11.00 0/10 PENDING\n")
