from __future__ import annotations

from typing import TYPE_CHECKING

from eth_typing import ChecksumAddress
from loguru import logger

from models.contract_raw import ContractRaw
from utils.utils import to_checksum

if TYPE_CHECKING:
    from models import Chain


class TokenTypes:
    ERC20 = 'erc20'
    NATIVE = 'native'
    STABLE = 'stable'


class Token(ContractRaw):


    def __init__(
            self,
            symbol: str,
            address: str,
            chain: Chain,
            decimals: int = 18,
            type_token: str = TokenTypes.ERC20,
            abi_name: str = 'erc20'
    ):
        super().__init__(address, abi_name, chain)
        self.symbol = symbol
        self.decimals = decimals
        self.type_token = type_token
        self.abi_name = abi_name

    def __str__(self) -> ChecksumAddress:
        return self.address

    def __eq__(self, other) -> bool:
        if isinstance(other, Token):
            return self.address == other.address
        elif isinstance(other, str):
            if other.startswith('0x'):
                return self.address == to_checksum(other)
            else:
                return self.symbol.upper() == other.upper()
        logger.error(f'Ошибка сравнения токенов {type(other)}')
        return False
