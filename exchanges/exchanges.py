from core.exchanges.okx import Okx
from core.exchanges.binance import Binance
from models.account import Account


class Exchanges:

    def __init__(self, account: Account) -> None:
        self.okx = Okx(account)
        self.binance = Binance(account)