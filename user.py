#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""
from orders import *
import logging


class User:
    def __init__(self, name, exchange):
        self.name = name
        self.exchange = exchange
        self.orders = []

        # extension
        self.cash = 0
        self.portfolio = {}

    def deposit(self, amount):
        self.cash += amount
        return self.cash

    def withdraw(self, amount):
        if amount > self.cash:
            raise Exception("Insufficient funds")
        
        self.cash -= min(amount, self.cash)
        return self.cash
    
    def get_balance(self):
        return self.cash
    
    def get_net_worth(self):
        portforlio_value = 0
        for ticker, quantity in self.portfolio.items():
            price = self.exchange.get_last_price(ticker)
            if price == 0:
                price, _ = self.exchange.get_bid_ask(ticker)
            portforlio_value += price * quantity
        return self.cash + portforlio_value

    def add_stock(self, ticker, quantity):
        self.portfolio.setdefault(ticker, 0)
        self.portfolio[ticker] += quantity

    def remove_stock(self, ticker, quantity):
        if ticker not in self.portfolio:
            raise Exception("No such stock in portfolio")
        elif self.portfolio[ticker] < quantity:
            raise Exception("Insufficient stock")
            
        self.portfolio[ticker] -= quantity

    def verify_order(self, order):
        # extension: check if the user has enough cash or stock
        if order.user != self:
            logging.critical("Order does not belong to this user")
            return False

        if isinstance(order, MarketOrder):
            cost = self.exchange.get_last_price(order.ticker) * order.quantity
        else:
            cost = order.price * order.quantity
        if order.direction == "BUY" and cost > self.cash:
            logging.critical("Insufficient funds")
            return False

        if order.direction == "SELL" and (not self.portfolio[order.ticker] or self.portfolio[order.ticker] < order.quantity):
            logging.critical("Insufficient stock")
            return False

        return True

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


class Admin(User):
    def __init__(self, name, exchange):
        super().__init__(name, exchange)

    def deposit(self, amount):
        self.cash += amount
        return self.cash

    def withdraw(self, amount):
        # cash would not go below 0
        self.cash -= min(amount, self.cash)
        return self.cash

    def add_stock(self, ticker, quantity):
        self.portfolio.setdefault(ticker, 0)
        self.portfolio[ticker] += quantity

    def remove_stock(self, ticker, quantity):
        # Stock quantity would not go below 0
        self.portfolio.setdefault(ticker, 0)
        self.portfolio[ticker] -= min(quantity, self.portfolio[ticker])

    def verify_order(self, order):
        if order.user != self:
            logging.critical("Order does not belong to this user")
            return False

        return True