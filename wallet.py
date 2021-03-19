import logging
from binance.client import Client

class Wallet:
    def __init__(self, **kwargs) -> None:
        self.client: Client = kwargs["client"]
        
        self.target = kwargs["amount"]
        self.cash   = kwargs["cash"]

        self.symbol = kwargs["symbol"]
        self.value = 0

        self.Update()

    def Update(self):
        self.value = float(self.client.get_avg_price(symbol=self.symbol)["price"])
        logging.info(f"Current market value for {self.symbol} is {self.value}.")
        
        return self.value

    def Buy(self, amount):
        self.Update()

        self.target += amount
        self.cash -= amount * self.value
        
        logging.info(f"Buying {amount} units in {self.symbol} for {amount * self.value}.")

        self.client.create_test_order(
            symbol=self.symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=amount
        )
    
    def Sell(self, amount):
        self.Update()

        self.target -= amount
        self.cash += amount * self.value
        
        logging.info(f"Selling {amount} units in {self.symbol} for {amount * self.value}.")

        self.client.create_test_order(
            symbol=self.symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=amount
        )