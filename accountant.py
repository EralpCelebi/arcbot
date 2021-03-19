import logging
from binance.client import Client
from wallet import Wallet

import time

CASH_AMOUNT = 40

class Accountant:
    def __init__(self, **kwargs) -> None:
        self.client: Client = kwargs["client"]
        self.wallet: Wallet = kwargs["wallet"]

        self.transactions = []

        self.last_direction = False
        self.current_direction = False
        
        self.last_value = self.wallet.value
        self.current_value = 0.0

        self.profit = 0.0
    
    def Update(self):
        self.last_value = self.current_value
        self.current_value = self.wallet.Update()

        if self.last_value < self.current_value:
            self.last_direction = self.current_direction
            self.current_direction = True
        else:
            self.last_direction = self.current_direction
            self.current_direction = False

    def Action(self):
        self.Update()

        if self.wallet.cash > float("{:.4f}".format(CASH_AMOUNT / self.current_value)):
            if self.last_direction == False and self.current_direction == True:
                bought_value  = self.current_value
                bought_amount = float("{:.4f}".format(CASH_AMOUNT / self.current_value))
                bought_cash   = bought_value * bought_amount
            
                self.transactions.append(
                    {"value":bought_value, "amount": bought_amount, "cash": bought_cash}
                )

                self.wallet.Buy(bought_amount)

                logging.info(f"Bought {bought_amount} {self.wallet.symbol} for {bought_cash} at {bought_value}")

        

        for transaction in self.transactions:
            if transaction["value"] < self.current_value:
                if not self.last_direction and self.current_direction:
                    self.wallet.Sell(transaction["amount"])
                    logging.info(f"Sold {transaction['amount']} {self.wallet.symbol} for {self.current_value}.")
                    
                    self.profit += self.current_value * transaction["amount"] - transaction["cash"]
                    logging.info(f"Current profit is {self.profit}.")
        
        
    def Initialise(self):
        for _ in range(2):
            time.sleep(10)
            self.Update()