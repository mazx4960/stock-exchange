#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""

class User:
    def __init__(self, name):
        self.name = name
        self.orders = []

    def place_order(self, order):
        self.orders.append(order)

    def view_orders(self):
        for ind, order in enumerate(self.orders):
            print(f"{ind+1}. {order}")
    
    def __str__(self) -> str:
        return self.name
