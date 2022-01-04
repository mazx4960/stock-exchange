#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@author: Desmond Tan
"""
import re
import heapq
from orders import *


BUY = 0
SELL = 1


class Exchange:
    def __init__(self):
        self.stocks = {}
        self.limit_orders = {}
        self.market_orders = {}
        self.trades = {}

    def list_stock(self, stock):
        """List the stock on the exchange."""
        if stock.ticker in self.stocks:
            raise Exception('Stock already exists')
        self.stocks[stock.ticker] = stock
        self.limit_orders[stock.ticker] = [[], []]
        self.market_orders[stock.ticker] = [[], []]
        self.trades[stock.ticker] = []

    def get_bid_ask(self, ticker):
        """Get the best bid and ask for a stock."""
        bid = self.limit_orders[ticker][BUY][0] if self.limit_orders[ticker][BUY] else None
        ask = self.limit_orders[ticker][SELL][0] if self.limit_orders[ticker][SELL] else None
        return bid, ask

    def get_last_price(self, ticker):
        """Get the last price of a stock."""
        last_trade = self.trades[ticker][-1] if self.trades[ticker] else None
        if last_trade:
            return last_trade.price
        return 0

    def place_limit_order(self, order):
        """Place a limit order on the exchange."""
        print(
            f"You have placed a limit {order.direction.lower()} order for {order.quantity} {order.ticker} shares at ${order.price:.2f} each.")
        self.resolve_order(order)
        return order

    def place_market_order(self, order):
        """Place a market order on the exchange."""
        print(
            f"You have placed a market order for {order.quantity} {order.ticker} shares.")
        self.resolve_order(order)
        return order

    def resolve_order(self, order):
        """Resolve an order on the exchange

        There are several constraints for an order to be resolved:
        1. The order will be first matched with the market orders before the limit orders.
        2. Market orders can only be matched with limit orders.
        3. Limit orders can be matched with limit orders if it is better than the bid or ask price.
        """
        if order.is_filled():
            return order

        direction = BUY if order.direction == "BUY" else SELL
        other_direction = SELL if direction == BUY else BUY
        limit_orders = self.limit_orders[order.ticker][other_direction]
        market_orders = self.market_orders[order.ticker][other_direction]

        # If the order is a limit order, check if there are any bids or asks that match the order
        bid, ask = self.get_bid_ask(order.ticker)
        if isinstance(order, LimitOrder) and not market_orders and order.direction == "BUY" and ask and ask.price > order.price:
            heapq.heappush(self.limit_orders[order.ticker][BUY], order)
            return order
        elif isinstance(order, LimitOrder) and not market_orders and order.direction == "SELL" and bid and bid.price < order.price:
            heapq.heappush(self.limit_orders[order.ticker][SELL], order)
            return order

        # Find a market order to match with the limit order
        # Cannot match market order with market order
        if isinstance(order, LimitOrder) and market_orders:
            other_order = market_orders[0]

        # Find a limit order to match with the market order or limit order
        elif limit_orders:
            other_order = self.limit_orders[order.ticker][other_direction][0]

        # No match
        else:
            if isinstance(order, MarketOrder):
                self.market_orders[order.ticker][direction].append(order)
            else:
                heapq.heappush(
                    self.limit_orders[order.ticker][direction], order)
            return order

        unfilled_quantity = order.quantity - order.filled
        filled_qty = other_order.fill(unfilled_quantity)
        order.fill(filled_qty)

        buyer = order.user if order.direction == "BUY" else other_order.user
        seller = order.user if order.direction == "SELL" else other_order.user
        price = other_order.price if isinstance(
            other_order, LimitOrder) else order.price
        self.trades[order.ticker].append(
            Trade(buyer, seller, price, filled_qty))

        # If the matching order is fully filled, pop it from the heap or queue
        if other_order.is_filled():
            if isinstance(other_order, MarketOrder):
                self.market_orders[order.ticker][other_direction].pop()
            else:
                heapq.heappop(
                    self.limit_orders[order.ticker][other_direction])

        return self.resolve_order(order)

    def execute(self, user, action):
        """Execute an action on the exchange

        An action is a string that would be parsed before being executed.
        """
        limit_order_re = r"^(BUY|SELL) (\w+) LMT \$([0-9]*[.]?[0-9]+) (\d+)$"
        match = re.match(limit_order_re, action)
        if match:
            direction, ticker, price, quantity = match.groups()
            if direction == 'BUY':
                order = BuyOrder(user, ticker, float(price), int(quantity))
            else:
                order = SellOrder(user, ticker, float(price), int(quantity))
            self.place_limit_order(order)
            user.place_order(order)
            return

        market_order_re = r"^(BUY|SELL) (\w+) MKT ([0-9]*[.]?[0-9]+)$"
        match = re.match(market_order_re, action)
        if match:
            direction, ticker, quantity = match.groups()
            order = MarketOrder(user, ticker, int(quantity), direction)
            self.place_market_order(order)
            user.place_order(order)
            return

        quote_re = r"^QUOTE (\w+)$"
        match = re.match(quote_re, action)
        if match:
            ticker = match.groups()[0]
            bid, ask = self.get_bid_ask(ticker)
            bid_price = bid.price if bid else 0
            ask_price = ask.price if ask else 0
            last_price = self.get_last_price(ticker)
            print(
                f"{ticker} BID: ${bid_price:.2f} ASK: ${ask_price:.2f} LAST: ${last_price:.2f}")
            return

        if action == 'VIEW ORDERS':
            user.view_orders()
            return


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker

    def __str__(self):
        return f"{self.ticker}"


class Trade:
    def __init__(self, buyer, seller, price, quantity):
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.buyer} bought {self.quantity} shares from {self.seller} at ${self.price:.2f} each."
