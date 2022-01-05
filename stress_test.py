#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
@author: Desmond Tan
"""
import random
from faker import Faker
import os

from orders import *
from exchange import *
from user import *


RESULTS_DIR = 'results'
ORDERS_FILE = os.path.join(RESULTS_DIR, 'orders.txt')
TRADES_FILE = os.path.join(RESULTS_DIR, 'trades.txt')
PRICES_FILE = os.path.join(RESULTS_DIR, 'prices.txt')


TICKERS = ['AAPL', 'MSFT', 'GOOG', 'FB', 'AMZN', 'SNAP']


def init_stocks(exchange, tickers=TICKERS):
    for ticker in tickers:
        exchange.list_stock(Stock(ticker))


def main():
    fake = Faker()

    exchange = Exchange()
    init_stocks(exchange)
    users = [Admin(fake.name(), exchange) for _ in range(100)]
    options = ['BUY', 'SELL', 'QUOTE', 'VIEW ORDERS']

    orders = []
    for _ in range(10000):
        user = random.choice(users)
        option = random.choice(options)
        if option == 'BUY' or option == 'SELL':
            ticker = random.choice(TICKERS)
            order_type = random.choices(['LMT', 'MKT'], weights=[0.9, 0.1], k=1)[0]
            quantity = random.randint(1, 100)
            if order_type == 'LMT':
                price = random.randint(1, 100)
                action = f"{option} {ticker} {order_type} ${price} {quantity}"
            else:
                action = f"{option} {ticker} {order_type} {quantity}"
            orders.append(str(user) + ': ' + action)
        elif option == 'QUOTE':
            action = option + ' ' + random.choice(TICKERS)
        else:
            action = option
        print(action)
        exchange.execute(user, action)
    
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    
    with open(ORDERS_FILE, 'w') as f:
        f.write("\n".join(orders))

    with open(TRADES_FILE, 'w') as f:
        for ticker in TICKERS:
            f.write(ticker + '\n')
            for trade in exchange.trades[ticker]:
                f.write(str(trade) + '\n')
    
    with open(PRICES_FILE, 'w') as f:
        for ticker in TICKERS:
            bid, ask = exchange.get_bid_ask(ticker)
            bid_price = bid.price if bid else 0
            ask_price = ask.price if ask else 0
            last_price = exchange.get_last_price(ticker)
            f.write(
                f"{ticker} BID: ${bid_price:.2f} ASK: ${ask_price:.2f} LAST: ${last_price:.2f}\n")


if __name__ == '__main__':
    main()
