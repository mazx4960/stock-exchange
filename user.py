#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""
from orders import *


class User:
    def __init__(self, name):
        self.name = name
        self.orders = []

        # extension
        self.cash = 0
        self.portfolio = {}

    def deposit(self, amount):
        self.cash += amount
        return self.cash

    def withdraw(self, amount):
        self.cash -= amount
        return self.cash

    def add_stock(self, ticker, quantity):
        self.portfolio.setdefault(ticker, 0)
        self.portfolio[ticker] += quantity

    def remove_stock(self, ticker, quantity):
        self.portfolio.setdefault(ticker, 0)
        self.portfolio[ticker] -= quantity

    def verify_order(self, order, exchange):
        # extension: check if the user has enough cash or stock
        if order.user != self:
            raise Exception("Order does not belong to this user")

        if isinstance(order, MarketOrder):
            cost = exchange.get_last_price(order.ticker) * order.quantity
        else:
            cost = order.price * order.quantity
        if order.direction == "BUY" and cost > self.cash:
            raise Exception("Insufficient funds")

        if order.direction == "SELL" and (not self.portfolio[order.ticker] or self.portfolio[order.ticker] < order.quantity):
            raise Exception("Insufficient stock")

    def place_order(self, order):
        self.orders.append(order)

    def view_orders(self):
        for ind, order in enumerate(self.orders):
            print(f"{ind+1}. {order}")
    
    def view_portfolio(self):
        print(f"{self.name}'s portfolio:")
        print(f"* Cash: ${self.cash:.2f}")
        for ticker, quantity in self.portfolio.items():
            print(f"* {ticker}: {quantity}")

    def __str__(self) -> str:
        return self.name
