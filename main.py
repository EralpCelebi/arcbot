import time
from accountant import Accountant
from binance.client import Client
import logging

from wallet import Wallet

API_KEY = ""
API_SECRET_KEY = ""

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

client = Client(API_KEY, API_SECRET_KEY)

wallet = Wallet(
    client=client,
    amount=0,
    cash=80,
    symbol="BTCTRY"
)

accountant = Accountant(
    client=client,
    wallet=wallet,
)

accountant.Initialise()

while True:
    accountant.Action()
    time.sleep(10)