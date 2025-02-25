from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from loguru import logger

from models.account import Account
from models.amount import Amount
from models.chain import Chain
from models.token import Token

from models.withdraw import WithdrawData

# класс для обмена валют
class AbsExchange(ABC):

    _chains: list[str] | set[str] = []

    @abstractmethod
    def __init__(self, account: Account) -> None:

        self.account = account
        pass

    @abstractmethod
    def get_chains(self) -> list:

        pass

    @abstractmethod
    def withdraw(
            self,
            *,
            token: Token | str,
            amount: Amount | int | float,
            chain: Chain | str,
            address: Optional[str] = None
    ) -> None:

        pass

    @abstractmethod
    def _wait_until_withdraw_complete(self, withdraw_id: str, timeout: int = 30) -> None:

        pass

    def _validate_inputs(
            self,
            token: Token | str,
            amount: Amount | int | float,
            chain: Chain | str,
            address: Optional[str]
    ) -> WithdrawData:


        if not address:
            address = self.account.address

        if isinstance(token, Token):
            token = token.symbol

        if isinstance(amount, Amount):
            amount = amount.ether

        chain = self._get_chain_name(chain)

        withdraw_data = WithdrawData(
            token=token,
            amount=amount,
            chain=chain,
            address=address
        )

        if not withdraw_data.is_valid:
            logger.error(f'{self.account.profile_number} [{self.__class__.__name__}] Переданы некорректные аргументы в withdraw(): {withdraw_data}')
            raise ValueError(f'Переданы некорректные аргументы в {self.__class__.__name__}.withdraw()')

        return withdraw_data

    def _get_chain_name(self, chain: Chain | str) -> str | None:

        if isinstance(chain, str):
            return chain

        if isinstance(chain, Chain):
            # получаем название биржи из имени класса
            exchange_name = self.__class__.__name__.lower()
            # ищем название сети для биржи в объекте сети
            chain_name = getattr(chain, f'{exchange_name}_name')

            if chain_name is None:
                logger.error(
                    f'{self.account.profile_number} [{self.__class__.__name__}] Вывод невозможен, у сети {chain.name} нет названия для')
            return chain_name

