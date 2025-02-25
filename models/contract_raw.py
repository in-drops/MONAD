from __future__ import annotations

import json
import os
from typing import Optional, TYPE_CHECKING

from eth_typing import ChecksumAddress
from loguru import logger

from config.settings import config
from utils.utils import to_checksum

if TYPE_CHECKING:
    from models import Chain


class ContractRaw:


    def __init__(self, address: str | ChecksumAddress, abi_name: str, chain: Chain):
        self.address = to_checksum(address)
        self.abi_name = abi_name
        self.chain = chain
        self._abi: Optional[list[dict]] = None

    def __str__(self):
        return self.address

    def __eq__(self, other) -> bool:
        if isinstance(other, ContractRaw):
            return self.address == other.address
        elif isinstance(other, str):
            if other.startswith('0x'):
                return self.address == to_checksum(other)
        logger.error(f'Ошибка сравнения контрактов {type(other)}')
        return False

    @property
    def abi(self) -> list[dict]:
        """
        Ленивый геттер abi контракта, загружает его из файла при первом обращении.
        :return: abi контракта
        """
        if not self._abi:
            path = os.path.join(config.PATH_ABI, f'{self.abi_name}.json')
            with open(path, 'r') as file:
                self._abi = json.load(file)
        return self._abi
