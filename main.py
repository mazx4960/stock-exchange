#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Desmond Tan

A Simple Stock Exchange
You're given the task of creating a simple stock exchange. It is so simple that it only supports a
limited set of functionality. However, there might be changes in the future.

Here are the functions that it should support:
  1. User is able place a buy order for a particular stock
  2. User is able place a sell order for a particular stock
  3. User is able to get the bid/ask and last price from the exchange
  4. User is able to place a limit order
  5. User is able to place a market order
  6. The exchange should be able to resolve the order. E.g. placing a buy limit order at price of
  $10 when the asking price is $9.99 will complete the trade.
  7. The user should be able to view all order status. E.g. filled, partially filled, pending.
  8. The user is able to exit the exchange program. (In real life, you exit the client)
"""
import random

from orders import *
from exchange import *
from user import *


TICKERS = ['AAPL', 'MSFT', 'GOOG', 'FB', 'AMZN', 'SNAP']


def init_stocks(exchange, tickers=TICKERS):
    for ticker in tickers:
        exchange.list_stock(Stock(ticker))


def init_order_books(exchange):
    user = User("admin", exchange)
    user.deposit(1000000)
    for ticker in TICKERS:
        user.add_stock(ticker, 100)
        mark_price = random.randint(2, 10)
        exchange.place_limit_order(BuyOrder(
            user, ticker, mark_price - 1, 100))
        exchange.place_limit_order(SellOrder(
            user, ticker, mark_price + 1, 100))


def main():
    exchange = Exchange()
    init_stocks(exchange)
    init_order_books(exchange)

    user = User("John", exchange)
    user.deposit(1000)

    while True:
        action = input("Action: ")
        if action == "QUIT":
            break
        exchange.execute(user, action)


if __name__ == '__main__':
    main()
