#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""


class Order:
    def __init__(self, user, ticker, quantity, direction):
        self.user = user
        self.ticker = ticker
        self.quantity = quantity
        self.direction = direction
        self.filled = 0

    def fill(self, quantity, price):
        """Fill the order with the given quantity.
        Ensures that the order is not filled beyond the quantity."""
        remaning = self.quantity - self.filled
        fill_quantity = min(remaning, quantity)
        self.filled += fill_quantity

        if self.direction == "BUY":
            self.user.withdraw(fill_quantity * price)
            self.user.add_stock(self.ticker, fill_quantity)
        else:
            self.user.remove_stock(self.ticker, fill_quantity)
            self.user.deposit(fill_quantity * price)
            
        return fill_quantity

    def is_filled(self):
        return self.filled == self.quantity

    def get_status(self):
        if self.is_filled():
            return "FILLED"
        elif self.filled > 0:
            return "PARTIAL"
        else:
            return "PENDING"


class MarketOrder(Order):
    def __init__(self, user, ticker, quantity, direction):
        super().__init__(user, ticker, quantity, direction)

    def __str__(self) -> str:
        status = self.get_status()
        return f"{self.ticker} MKT {self.direction} {self.filled}/{self.quantity} {status}"


class LimitOrder(Order):
    def __init__(self, user, ticker, price, quantity, direction):
        self.price = price
        super().__init__(user, ticker, quantity, direction)

    def __str__(self):
        status = self.get_status()
        return f"{self.ticker} LMT {self.direction} ${self.price:.2f} {self.filled}/{self.quantity} {status}"


class BuyOrder(LimitOrder):
    """Implemented such that the order with the highest price is always given priority"""

    def __init__(self, user, ticker, price, quantity):
        super().__init__(user, ticker, price, quantity, "BUY")

    def __lt__(self, other):
        return self.price > other.price


class SellOrder(LimitOrder):
    """Implemented such that the order with the lowest price is always given priority"""

    def __init__(self, user, ticker, price, quantity):
        super().__init__(user, ticker, price, quantity, "SELL")

    def __lt__(self, other):
        return self.price < other.price
