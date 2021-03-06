# Simple Stock Exchange 
![Coverage](https://img.shields.io/codecov/c/github/mazx4960/stock-exchange)

## Functionality
1. User is able place a buy order for a particular stock
2. User is able place a sell order for a particular stock
3. User is able to get the bid/ask and last price from the exchange
4. User is able to place a limit order
5. User is able to place a market order
6. The exchange should be able to resolve the order. E.g. placing a buy limit order at price of $10 when the asking price is $9.99 will complete the trade.
7. The user should be able to view all order status. E.g. filled, partially filled, pending.
8. The user is able to exit the exchange program. (In real life, you exit the client)

## Usage

Python3 is required. Run `pip -r requirements.txt` to install all the dependencies (if any).

### Running the program
```sh
python3 main.py
```

### Testing the program
```sh
python3 -m unittest
```

## Problems
- [x] Market orders matching with market orders (no indicative price)

## Extensions
- [x] Each user have their own account and balance
- [ ] Allow users to track their profits and losses
- [ ] Getting trade graph 

