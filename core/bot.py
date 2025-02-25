from loguru import logger

from core.browser import Ads, Metamask
from core.excel import Excel
from core.exchanges import Exchanges
from core.onchain import Onchain
from models.chain import Chain
from models.account import Account
from config import config


class Bot:
    def __init__(self, account: Account, chain: Chain = config.start_chain) -> None:
        logger.info(f'{account.profile_number} Запуск профиля!')
        self.chain = chain
        self.account = account
        self.ads = Ads(account)
        self.excel = Excel(account)
        self.metamask = Metamask(self.ads, account, self.excel)
        self.exchanges = Exchanges(account)
        self.onchain = Onchain(account, self.chain)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.ads.close_browser()
        if exc_type is None:
            logger.success(f'{self.account.profile_number} Аккаунт завершен успешно!')
        elif issubclass(exc_type, TimeoutError):
            logger.error(f'{self.account.profile_number} Аккаунт завершен по таймауту!')
        else:
            if 'object has no attribute: page' in str(exc_val):
                logger.error(f'{self.account.profile_number} Аккаунт завершен с ошибкой, возможно вы '
                             f'выключили работу браузера и пытаетесь сделать логику работу с браузером. {exc_val}')
            else:
                logger.critical(f'{self.account.profile_number} Аккаунт завершен с ошибкой: {exc_val}')
        return True
